import FinanceDataReader as fdr
import pandas as pd
import matplotlib.pyplot as plt
import multiprocessing

import FinanceDataReader as fdr

marcap_df = fdr.StockListing('krx-marcap')
marcap_df.iloc[0]

# # plt.rcParams["font.family"] = 'nanummyeongjo'
# plt.rcParams['font.family'] ='Malgun Gothic'
# plt.rcParams['axes.unicode_minus'] =False

# plt.rcParams["figure.figsize"] = (14,4)
# plt.rcParams['lines.linewidth'] = 2
# plt.rcParams["axes.grid"] = True

df = pd.read_csv('upjong.csv')

group_df_list = []
def getDiffMarCap(group):
    try:
        print(group)
        code_price_list = []        
        for i,item in group.iterrows():
            _,cate,name,code = item            
            code_df = fdr.DataReader(code,'2024')
            code_df['cate']=cate
            code_df['code']=code
            code_df['name']=name
            code_price_list.append(code_df)
        
        concated_df = pd.concat(code_price_list).reset_index()
        marcap_cols = ['Code','Stocks']
        stocks_df = marcap_df[marcap_cols]
        merged_df = pd.merge(concated_df,stocks_df,left_on=['code'],right_on=['Code'])
        merged_df['Marcap'] = merged_df[['Stocks','Close']].apply(lambda x : x['Stocks'] * x['Close'],axis=1)
        merged_df = merged_df.set_index('Date')
        summary_df = merged_df.groupby(merged_df.index)['Marcap'].sum().to_frame()
        summary_df['Pct'] = summary_df.pct_change()*100
        summary_df['Cate'] = cate
        summary_df.index = summary_df.index.date
        group_df_list.append(summary_df)
    except Exception as e:
        return pd.DataFrame()


df.groupby('category').apply(getDiffMarCap)
all_df = pd.concat(group_df_list)
all_df.to_csv('upjong_summary.csv',encoding='utf-8')

# for i,samples in df.groupby('category'):
#     code_price_list = []
#     for i,item in samples.iterrows():
#         _,cate,name,code = item
#         code_df = fdr.DataReader(code,'2024')
#         code_df['cate']=cate
#         code_df['code']=code
#         code_df['name']=name
#         code_price_list.append(code_df)

#     concated_df = pd.concat(code_price_list).reset_index()
#     marcap_cols = ['Code','Stocks']
#     stocks_df = marcap_df[marcap_cols]
#     merged_df = pd.merge(concated_df,stocks_df,left_on=['code'],right_on=['Code'])
#     merged_df['Marcap'] = merged_df[['Stocks','Close']].apply(lambda x : x['Stocks'] * x['Close'],axis=1)
#     merged_df = merged_df.set_index('Date')
#     summary_df = merged_df.groupby(merged_df.index)['Marcap'].sum().to_frame()
#     summary_df['Pct'] = summary_df.pct_change()*100
#     summary_df['Cate'] = cate
#     summary_df.index = summary_df.index.date
#     fig, ax1 = plt.subplots()

#     # 첫 번째 서브플롯 (선 그래프)
#     color = 'tab:red'
#     ax1.set_xlabel('Date')
#     ax1.set_ylabel('시가총액', color=color)
#     ax1.plot(summary_df.index, summary_df['Marcap'], color=color)
#     ax1.tick_params(axis='y', labelcolor=color)

#     # 두 번째 서브플롯 (막대 그래프)
#     ax2 = ax1.twinx()  
#     color = 'tab:blue'
#     ax2.set_ylabel('시총변화율', color=color)
#     ax2.bar(summary_df.index, summary_df['Pct'], color=color, alpha=0.5)
#     ax2.tick_params(axis='y', labelcolor=color)

#     # 그래프 타이틀 설정
#     plt.title(cate)
#     # 그래프 출력
#     plt.show()