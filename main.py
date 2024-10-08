import time
import argparse
import numpy as np
import pandas as pd
import baselines
import torch
from torchvision import datasets
from torch import nn, optim, autograd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, LogisticRegression
from models import Causal_model_vae
from sklearn.metrics import accuracy_score, mean_squared_error, mean_absolute_error, f1_score
import utils
import pickle
import torch.nn.functional as F
import warnings
import logging

# 忽略所有警告
warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser(description='Counterfactual fairness with no explicit prior knowledge')
parser.add_argument('-cuda', '--cudanum', type=int, default=1, help='Disables CUDA training.')
parser.add_argument('--dataset', default='law', help='Dataset name')  # 'law', 'adult'
parser.add_argument('--synthetic', type=int, default=1, help='Whether to use synthetic dataset')
parser.add_argument('--seed', type=int, default=1, metavar='S',
                    help='random seed (default: 1)')
parser.add_argument('-t', '--training', type=int, default=1, help='Whether start training.')
parser.add_argument('--pyromodel', default='models_save/cfpup.pt', help='Dataset models')
parser.add_argument('--pyroparam', default='models_save/cfpup_param.pt', help='Dataset params')
parser.add_argument('--lrcausalmodel', type=float, default=0.001,
                    help='learning rate for causal mode')
parser.add_argument('-a', '--alpha', type=float, default=10000,
                    help='alpha for custom loss')

parser.add_argument('--num_iterations_causalmodel', '-iter', type=int, default=12000, metavar='N',  # synthetic: 10000, law/adult: 12000
                    help='number of epochs to train causal model (default: 10)')
parser.add_argument('--epochs_vae', type=int, default=10, metavar='N', help='number of epochs to train (default: 10)')

parser.add_argument('--decoder_type', default='together', help='decoder type in vae')  # 'together', 'separate'
parser.add_argument('--lr', type=float, default=2e-3, help='learning rate for optimizer')
args = parser.parse_args()

syn = 'synthetic' if args.synthetic else 'real'
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,  # 控制台打印的日志级别
                    filename='logs/' + f"{syn}_{args.dataset}_seed{args.seed}_" + f"iter{args.num_iterations_causalmodel}_" + f"alpha{args.alpha}_" + time.strftime('%m-%d-%H:%M:%S',time.localtime(time.time())) + '.log',
                    filemode='w',  
                    format='%(asctime)s: %(message)s'# 日志格式
                    )
logger.info(args)
# select gpu if available
args.cuda = not (args.cudanum == -1) and torch.cuda.is_available()
device = torch.device(f"cuda:{args.cudanum}" if args.cuda else "cpu")
args.device = device

# seed
np.random.seed(args.seed)
torch.manual_seed(args.seed)

def get_cf_pred(model_name, model, data_cf_tst, s_cf):
    y_pred_cf = []  # S x n
    for si in range(len(s_cf)):

        if args.dataset == 'law':
            if model_name == 'full':
                x_fair = torch.cat([data_cf_tst[si]['LSAT'].view(-1, 1), data_cf_tst[si]['UGPA'].view(-1, 1),
                                    data_cf_tst[si]['race'].view(-1, 1)], dim=1).cpu().detach().numpy()
            elif model_name == 'unaware':
                x_fair = torch.cat([data_cf_tst[si]['LSAT'].view(-1, 1), data_cf_tst[si]['UGPA'].view(-1, 1)], dim=1).cpu().detach().numpy()
            elif model_name == 'constant':
                tst_size = len(data_cf_tst[si]['LSAT'])
                y_pred_si = np.full((tst_size, 1), model)
            elif model_name == 'cfpup':
                if args.synthetic != 0:
                    x_fair = data_cf_tst[si]['knowledge'].view(-1, 1).cpu().detach().numpy()  # n x 1
                else:
                    x_fair = data_cf_tst[si]['knowledge_cfpup'].view(-1, 1).cpu().detach().numpy()  # n x 1
            elif model_name == 'cfpu':
                if args.synthetic != 0:
                    x_fair = data_cf_tst[si]['knowledge'].view(-1, 1).cpu().detach().numpy()  # n x 1
                else:
                    x_fair = data_cf_tst[si]['knowledge_cfpu'].view(-1, 1).cpu().detach().numpy()  # n x 1
                
        elif args.dataset == 'adult':
            if model_name == 'full':
                x_fair = torch.cat([data_cf_tst[si]['Sex'], data_cf_tst[si]['MaritalStatus'],
                     data_cf_tst[si]['Occupation'], data_cf_tst[si]['EducationNum'],
                     data_cf_tst[si]['HoursPerWeek'], data_cf_tst[si]['Race']], dim=1).cpu().detach().numpy()
            elif model_name == 'cfpu':
                #x_fair = data_latent_list.cpu().detach().numpy()  # n x 1
                if args.synthetic != 0:
                    x_fair = torch.cat([data_cf_tst[si]['Sex'], data_cf_tst[si]['eps_MaritalStatus'],data_cf_tst[si]['eps_EducationNum'],
                                    data_cf_tst[si]['eps_Occupation'],data_cf_tst[si]['eps_HoursPerWeek'],
                                    data_cf_tst[si]['eps_Income']],dim=1).cpu().detach().numpy()  # n x 1
                else:
                    x_fair = torch.cat([data_cf_tst[si]['Sex'], data_cf_tst[si]['eps_MaritalStatus_cfpu'],data_cf_tst[si]['eps_EducationNum_cfpu'],
                                    data_cf_tst[si]['eps_Occupation_cfpu'],data_cf_tst[si]['eps_HoursPerWeek_cfpu'],
                                    data_cf_tst[si]['eps_Income_cfpu']],dim=1).cpu().detach().numpy()  # n x 1
                
            elif model_name == 'cfpup':
                #x_fair = data_latent_list.cpu().detach().numpy()  # n x 1
                if args.synthetic != 0:
                    x_fair = torch.cat([data_cf_tst[si]['Sex'], data_cf_tst[si]['eps_MaritalStatus'],data_cf_tst[si]['eps_EducationNum'],
                                    data_cf_tst[si]['eps_Occupation'],data_cf_tst[si]['eps_HoursPerWeek'],
                                    data_cf_tst[si]['eps_Income']],dim=1).cpu().detach().numpy()  # n x 1
                else:
                    x_fair = torch.cat([data_cf_tst[si]['Sex'], data_cf_tst[si]['eps_MaritalStatus_cfpup'],data_cf_tst[si]['eps_EducationNum_cfpup'],
                                    data_cf_tst[si]['eps_Occupation_cfpup'],data_cf_tst[si]['eps_HoursPerWeek_cfpup'],
                                    data_cf_tst[si]['eps_Income_cfpup']],dim=1).cpu().detach().numpy()  # n x 1
            elif model_name == 'unaware':
                x_fair = torch.cat([data_cf_tst[si]['Sex'], data_cf_tst[si]['MaritalStatus'],
                                    data_cf_tst[si]['Occupation'], data_cf_tst[si]['EducationNum'],
                                    data_cf_tst[si]['HoursPerWeek']], dim=1).cpu().detach().numpy()
            elif model_name == 'constant':
                tst_size = len(data_cf_tst[si]['Sex'])
                y_pred_si = np.full((tst_size, 1), model)

        if model_name != 'constant':
            if args.dataset == 'adult':  # y_prob
                y_pred_si = model.predict_proba(x_fair)[:, 1]
            else: # y_hat
                y_pred_si = model.predict(x_fair)
            
        y_pred_cf.append(y_pred_si)  # n x 1
    return y_pred_cf

def eval_fairness(y_pred_cf_raw, type=1,  p_mmd=0.003, s_wass=0.005):
    y_pred_cf = y_pred_cf_raw.copy()
    MMD_dict = {}
    wass_dict = {}
    for i in range(len(y_pred_cf)):  # each S
        for j in range(i+1, len(y_pred_cf)):
            mmd = utils.mmd_linear(torch.FloatTensor(y_pred_cf[i].reshape(-1,1)).to(args.device), torch.FloatTensor(y_pred_cf[j].reshape(-1,1)).to(args.device), p=p_mmd)
            wass, _ = utils.wasserstein(torch.FloatTensor(y_pred_cf[i].reshape(-1,1)).to(args.device), torch.FloatTensor(y_pred_cf[j].reshape(-1,1)).to(args.device), args.device, cuda=True, scal=s_wass)

            MMD_dict[str(i)+'_'+str(j)] = mmd.item()
            wass_dict[str(i)+'_'+str(j)] = wass.item()

    MMD_list = [MMD_dict[k] for k in MMD_dict]
    wass_list = [wass_dict[k] for k in wass_dict]
    MMD_dict['Average'] = (sum(MMD_list) / len(MMD_list))
    wass_dict['Average'] = (sum(wass_list) / len(wass_list))
    eval_result = {'MMD': MMD_dict, 'Wass': wass_dict}
    return eval_result

def evaluate_model(y_true, y_pred, metrics):
    # y_true, y_pred: n_sample
    eval_result = {}
    if 'F1-score' in metrics:
        eval_result['F1-score'] = f1_score(y_true, y_pred)
    if 'Accuracy' in metrics:
        eval_result['Accuracy'] = accuracy_score(y_true, y_pred)
    if 'RMSE' in metrics:
        eval_result['RMSE'] = np.sqrt(mean_squared_error(y_true, y_pred))
    if 'MAE' in metrics:
        eval_result['MAE'] = mean_absolute_error(y_true, y_pred)
    return eval_result

def load_data(path, dataset):
    if dataset == 'synthetic':
        with open(path, 'rb') as f:
            data_save = pickle.load(f)
        n = data_save['data']['X_0'].shape[0]
    elif dataset == 'law':
        data_save = utils.load_data(path, dataset)
        n = data_save['data']['race'].shape[0]
    elif dataset == 'adult':
        data_save = utils.load_data(path, dataset)
        n = data_save['data']['Race'].shape[0]
    trn_idx_list, val_idx_list, tst_idx_list = utils.split_data(n, rates=[0.8, 0.1, 0.1], type='random', sorted=True, seed = args.seed)
    data_save['index'] = {'trn_idx_list': trn_idx_list, 'val_idx_list': val_idx_list, 'tst_idx_list': tst_idx_list}
    
    return data_save



def train_models(data_save, metrics_set, type='linear'):
    # data_save contains numpy
    if args.dataset == 'law':
        x = np.concatenate([data_save['data']['LSAT'], data_save['data']['UGPA']], axis=1)
        y = data_save['data']['ZFYA']
        env = data_save['data']['race']
        type='linear'
    elif args.dataset == 'adult':
        x = np.concatenate([data_save['data']['Sex'], data_save['data']['MaritalStatus'], data_save['data']['Occupation'],
                            data_save['data']['EducationNum'], data_save['data']['HoursPerWeek']], axis=1)
        y = data_save['data']['Income']
        env = data_save['data']['Race']
        type = 'logistic'
        
    train_idx = data_save['index']['trn_idx_list']
    val_idx = data_save['index']['val_idx_list']
    test_idx = data_save['index']['tst_idx_list']
    
    y_pred_tst_constant = baselines.run_constant(x, y.reshape(-1), train_idx, test_idx, type)
    eval_constant = evaluate_model(y[test_idx].reshape(-1), y_pred_tst_constant, metrics_set)
    logger.info(f"=========== evaluation for constant predictor ================: {eval_constant}")

    y_pred_tst_full, clf_full = baselines.run_full(x, y.reshape(-1), env, train_idx, test_idx, type)
    eval_full = evaluate_model(y[test_idx].reshape(-1), y_pred_tst_full, metrics_set)
    logger.info(f"=========== evaluation for full predictor ================: {eval_full}")

    y_pred_tst_unaware, clf_unaware = baselines.run_unaware(x, y.reshape(-1), train_idx, test_idx, type)
    eval_unaware = evaluate_model(y[test_idx].reshape(-1), y_pred_tst_unaware, metrics_set)
    logger.info(f"=========== evaluation for unaware predictor ================: {eval_unaware}")
    
    y_pred_cfpu, clf_cfpu, data_return_cfpu = baselines.run_cfp_u(data_save, train_idx, test_idx, type, device)
    eval_cfpu = evaluate_model(y[test_idx].reshape(-1), y_pred_cfpu, metrics_set)
    logger.info(f"=========== evaluation for cfp_u predictor ================: {eval_cfpu}")
    
    y_pred_cfpup, clf_cfpup, data_return_cfpup = baselines.run_cfp_up(data_save, train_idx, test_idx, type, device)
    eval_cfpup = evaluate_model(y[test_idx].reshape(-1), y_pred_cfpup, metrics_set)
    logger.info(f"=========== evaluation for cfp_up predictor ================: {eval_cfpup}")
    return {'clf_full': clf_full, 'clf_unaware': clf_unaware, 'constant_y': y_pred_tst_constant[0], 'clf_cfpu':clf_cfpu, 'clf_cfpup': clf_cfpup}, data_return_cfpu, data_return_cfpup

def get_test_dataset(dataset, y_pred_cfpup):
    dataset_test ={}
    test_index = dataset['index']['tst_idx_list']
    for key, value in dataset['data'].items():
        dataset_test[key] = value[test_index].reshape(-1)
    dataset_test['y_pred_cfpup'] = torch.from_numpy(y_pred_cfpup).to(device)
    return dataset_test

def norm_mse(pred, true):
    mean = torch.mean(true, dim=0)
    std = torch.std(true, dim=0)
    norm_pred = (pred - mean) / std
    norm_true = (true - mean) / std
    loss_mse = torch.mean(torch.pow(norm_pred - norm_true, 2), dim=0)
    loss_mse = loss_mse.sum()
    return loss_mse

def loss_function_vae(return_result, data, data_s, s_cf):
    h = return_result['mu_h']
    mu_h = h
    logvar_h = return_result['logvar_h']
    data_reconst = return_result['reconstruct']

    # representation balancing
    num_ij = 0
    mmd_loss = 0.0
    for i in range(len(s_cf)):
        idx_si = torch.where(data_s.view(-1) == i)  # index
        for j in range(i+1, len(s_cf)):
            idx_sj = torch.where(data_s.view(-1) == j)  # index
            num_ij += 1
            mmd_loss += utils.mmd_linear(h[idx_si], h[idx_sj], p=10)
    mmd_loss /= num_ij

    # reconstruct loss
    loss_r = norm_mse(data_reconst, data)

    KL = torch.mean(-0.5 * torch.sum(1 + logvar_h - mu_h.pow(2) - logvar_h.exp(), dim=1), dim=0)

    loss = loss_r + args.alpha * mmd_loss + KL

    eval_result = {'loss': loss, 'loss_r': loss_r, 'loss_mmd': mmd_loss, 'loss_kl': KL}
    return eval_result

def test_vae(model, idx_select, data, data_s, s_cf):
    model.eval()
    return_result = model(data[idx_select], data_s[idx_select])
    eval_result = loss_function_vae(return_result, data[idx_select], data_s[idx_select], s_cf)
    return eval_result

def map_cf_out(data_cf, latent_var, dataset):
    # data_cf: n x dim_x
    data = dict()
    if dataset == 'law':
        data['LSAT'] = data_cf[:, 0].view(-1)
        data['UGPA'] = data_cf[:, 1].view(-1)
        n = len(data['LSAT'])
        data['knowledge'] = latent_var.view(n, -1)
        if data['knowledge'].shape[1] == 1:
            data['knowledge'] = data['knowledge'].view(-1)
        data['ZFYA'] = data_cf[:, 2].view(-1)
    if dataset == 'adult':
        data['Sex'] = data_cf[:, :2]
        data['MaritalStatus'] = data_cf[:, 2:9]
        data['Occupation'] = data_cf[:, 9:23]
        data['EducationNum'] = data_cf[:, 23].view(-1, 1)
        data['HoursPerWeek'] = data_cf[:, 24].view(-1, 1)
        data['Income'] = data_cf[:, 25].view(-1, 1)

        data['eps_MaritalStatus'] = latent_var[:, 0].view(-1,1)
        data['eps_EducationNum'] = latent_var[:, 1].view(-1,1)
        data['eps_Occupation'] = latent_var[:, 2].view(-1,1)
        data['eps_HoursPerWeek'] = latent_var[:, 3].view(-1,1)
        data['eps_Income'] = latent_var[:, 4].view(-1,1)

    return data

def get_intervene_data_vae(cm_vae, s_cf, dataset, data_vae, S_name, type='kv', num_sample=1):  # type=kv, raw
    x_cf_list = []  # num_sample x S x n x d, tensor;
    n = data_vae.shape[0]
    for sample_i in range(num_sample):
        x_cf_allS = []
        for i in range(len(s_cf)):
            data_s = torch.full(size=(n, 1), fill_value=s_cf[i]).to(device)
            return_result = cm_vae(data_vae, data_s)  # n x d
            data_cf, latent_var = return_result['reconstruct'], return_result['h_sample']  # x_cf, y_cf

            if type == 'kv':
                data_cf_kv = map_cf_out(data_cf, latent_var, dataset)
                x_cf_allS.append(data_cf_kv)
            else:
                x_cf = data_cf[:, :-1]  # exclude y
                x_cf_allS.append(x_cf)
        x_cf_list.append(x_cf_allS)
    return x_cf_list

def in_train_vae(epochs, model, optimizer, data, data_s, s_cf, trn_idx, val_idx, tst_idx):
    time_begin = time.time()
    model.train()

    for epoch in range(epochs):
        optimizer.zero_grad()
        return_result = model(data[trn_idx], data_s[trn_idx])
        eval_result = loss_function_vae(return_result, data[trn_idx], data_s[trn_idx], s_cf)
        loss, loss_r, loss_mmd, loss_kl = eval_result['loss'], eval_result['loss_r'], eval_result['loss_mmd'], eval_result['loss_kl']

        loss.backward()
        optimizer.step()

        if epoch % 100 == 0:
            model.eval()
            eval_result_tst = test_vae(model, tst_idx, data, data_s, s_cf)
            loss_test = eval_result_tst['loss'].item()
            logger.info(f'Epoch: {epoch + 1:04d}, loss_train: {loss.item():.4f}, loss_test: {loss_test:.4f}, time: {(time.time() - time_begin):.4f}s')
            model.train()

    return model

def train_vae(dataset, s_f, s_feature, path_cae_model):
    if args.dataset == 'law':
        data_vae = torch.cat([dataset['data']['LSAT'], dataset['data']['UGPA'], dataset['data']['ZFYA']], dim=1)
        dim_x = data_vae.shape[1]
        model = Causal_model_vae(dim_x, len(s_feature), 1)
    elif args.dataset == 'adult':
        data_vae = torch.cat([dataset['data']['Sex'], dataset['data']['MaritalStatus'], dataset['data']['Occupation'],
                 dataset['data']['EducationNum'], dataset['data']['HoursPerWeek'], dataset['data']['Income']], dim=1)
        dim_x = data_vae.shape[1]
        model = Causal_model_vae(dim_x, len(s_feature), 5)
        
    trn_idx, val_idx, tst_idx = dataset['index']['trn_idx_list'], dataset['index']['val_idx_list'], dataset['index']['tst_idx_list']
    if args.training:
        # train vae
        optimizer_vae = optim.Adam(model.parameters(), lr=args.lr)
        in_train_vae(args.epochs_vae, model, optimizer_vae, data_vae, dataset['data'][s_f], s_feature, trn_idx, val_idx, tst_idx)
        torch.save(model.state_dict(), path_cae_model)
        logger.info(f'saved VAE model in: {path_cae_model}')

    else:  # load
        model.load_state_dict(torch.load(path_cae_model))
        logger.info(f'loaded VAE model from: {path_cae_model}')
        
    data_vae_select = data_vae[tst_idx,:]
    data_cf_vae = get_intervene_data_vae(model, s_feature, args.dataset, data_vae_select, s_f[0], type='kv', num_sample=1)[0]
    return data_cf_vae

def main(path):
    dataset = load_data(path, args.dataset)  # environment selection
    if args.dataset == 'law':
        metrics_set = set({"RMSE", "MAE"})
        S_name = 'race'
        s_feature = [0.0, 1.0, 2.0]
    elif args.dataset == 'adult':
        metrics_set = set({"Accuracy", 'F1-score'})
        S_name = 'Race'
        s_feature = [0.0, 1.0, 2.0]
    
    # performance analysis
    models, latentData_cfpu, latentData_cfpup = train_models(dataset, metrics_set, 'linear')
    latentData_cfpu = {key + '_cfpu': value.unsqueeze(1) for key, value in latentData_cfpu.items()}
    latentData_cfpup = {key + '_cfpup': value.unsqueeze(1) for key, value in latentData_cfpup.items()}
    model_dict = {'constant': models['constant_y'], 'full': models['clf_full'],
                      'unaware': models['clf_unaware'], 'cfpu':models['clf_cfpu'], 'cfpup': models['clf_cfpup']}
    # fairness analysis
    # 1. Counterfactual model generation
    
    if args.synthetic != 0:
        dataset_test_s = train_vae(dataset, S_name, s_feature, 'models_save/vae.pt')
        dataset_test_s = [
        {**item, S_name: torch.full((next(iter(item.values())).shape[0], 1), i).to(device)} 
        for i, item in enumerate(dataset_test_s)
        ]
    else:
        data_save_test ={}
        test_index = dataset['index']['tst_idx_list']
        
        dataset['data'].update(latentData_cfpu)
        dataset['data'].update(latentData_cfpup)
        if args.dataset == 'law':
            for key, value in dataset['data'].items():
                data_save_test[key] = value[test_index]
            dataset_test_s = [
                {key: torch.tensor(data_save_test[key][data_save_test[S_name] == r]) for key in data_save_test}
                for r in s_feature
                ]
        elif args.dataset == 'adult':
            for key, value in dataset['data'].items():
                data_save_test[key] = value[test_index, :]
            
            dataset_test_s = [
                {key: torch.tensor(data_save_test[key][data_save_test[S_name].view(-1) == r, :]) for key in data_save_test}
                for r in s_feature
                ]
            
    for model_name in model_dict:
        model = model_dict[model_name]
        y_pred_cf = get_cf_pred(model_name, model, dataset_test_s, s_feature)  # list, size = S, each elem: n_select
        eval_fair_result = eval_fairness(y_pred_cf, p_mmd=0.003, s_wass=0.005)
        logger.info(model_name)
        logger.info(eval_fair_result)

if __name__ == '__main__':
    if args.dataset == 'law':
        path = './dataset/law_data.csv'
    elif args.dataset == 'adult':
        path = './dataset/adult.data'
    main(path)
