import  os
import pandas as pd
from sqlalchemy import create_engine
from pyecharts import options as opts
from pyecharts.charts import Pie, Line, Bar, Liquid

engine = create_engine('mysql+pymysql://user:123456@localhost:3306/more_date?charset=utf8')
#付费用户占比
sql = """
select sum(if(pay_price > 0,1,0))as '付费',sum(if(pay_price = 0,1,0))as '非付费'
from game_data
"""
data = pd.read_sql(con=engine, sql=sql)
c1 = (
    Pie()
    .add(
        "",
        [list(z) for z in zip(data.columns, data.values[0])],
    )
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c} 占比: {d}%"))
    .render("付费用户占比.html")
)
os.system("付费用户占比.html")
#日新增用户
sql = """
select cast(register_time as date) as "day" , count(1) as 'user' from game_data
group by cast(register_time as date) order by day
"""
data  = pd.read_sql(con = engine,sql = sql)
c2 = (
    Bar()
    .add_xaxis(list(data['day']))
    .add_yaxis("新增用户数",list(data['user']))
    .set_global_opts(title_opts=opts.TitleOpts(title="每日新增用户数"))
    .render("日新增用户.html")
)
os.system("日新增用户.html")
#小时新增用户占比
sql = """
SELECT hour(register_time) as xs,count(*) as user FROM game_data 
group by hour(register_time) order by hour(register_time)
"""
data  = pd.read_sql(con=engine,sql = sql)
c3 =(
    Line()
    .add_xaxis(list(data['xs']))
    .add_yaxis("新增用户数",list(data['user']))
    .set_global_opts(title_opts=opts.TitleOpts(title="每小时新增用户数"))
    .render("每小时新增用户.html")
)
os.system("每小时新增用户.html")
#用户在线时长
sql = """
select  avg(avg_online_minutes) as "平均在线时长" ,
sum(case when pay_price > 0 then avg_online_minutes else 0 end) / 
sum(case when pay_price > 0 then 1 else 0 end) as `付费玩家在线时长`,
sum(case when pay_price > 0 then 0 else avg_online_minutes end) / 
sum(case when pay_price > 0 then 0 else 1 end) as `非付费玩家在线时长`
 from more_date.game_data
"""
data = pd.read_sql(con=engine,sql = sql)
c4 = (
    Bar()
    .add_xaxis(list(data.columns))
    .add_yaxis("平均在线时长(单位:分钟)",list(data.values[0]))
    .set_global_opts(title_opts=opts.TitleOpts(title="平均在线时长"))
    .render("在线时长.html")
)
os.system("在线时长.html")
#活跃付费人数占活跃人数比例
sql = """
select sum(case when avg_online_minutes >0 and pay_price >0 then 1 else 0 end) /
sum(case when avg_online_minutes >0  then 1 else 0 end) as "活跃付费人数占活跃人数比例"
from more_date.game_data
"""
data = pd.read_sql(con=engine,sql = sql)
c5 = (
    Liquid()
    .add("比例",[data['活跃付费人数占活跃人数比例'][0]])
    .set_global_opts(title_opts=opts.TitleOpts(title="活跃付费人数占活跃人数比例"))
    .render("活跃付费人数占活跃人数比例.html")
)
os.system("活跃付费人数占活跃人数比例.html")
#不同类别用户胜率
sql = """
select 'PVP' as `游戏类型`,
       sum(pvp_win_count) / sum(pvp_battle_count) as `平均胜率`,
       sum(case when pay_price > 0 then pvp_win_count else 0 end) / sum(case when pay_price > 0 then pvp_battle_count else 0 end) as `付费用户胜率`,
       sum(case when pay_price = 0 then pvp_win_count else 0 end) / sum(case when pay_price = 0 then pvp_battle_count else 0 end) as `非付费用户胜率`
from more_date.game_data
union all
select 'PVE' as `游戏类型`,
       sum(pve_win_count) / sum(pve_battle_count) as `平均胜率`,
       sum(case when pay_price > 0 then pve_win_count else 0 end) / sum(case when pay_price > 0 then pve_battle_count else 0 end) as `付费用户胜率`,
       sum(case when pay_price = 0 then pve_win_count else 0 end) / sum(case when pay_price = 0 then pve_battle_count else 0 end) as `非付费用户胜率`
from more_date.game_data
"""
data = pd.read_sql(con=engine,sql = sql)
c6 = (
    Bar()
    .add_dataset(
        source=[data.columns.tolist()] + data.values.tolist()
    )
    .add_yaxis(series_name="平均胜率",y_axis=[])
    .add_yaxis(series_name="付费用户胜率",y_axis=[])
    .add_yaxis(series_name="非付费用户胜率",y_axis=[])
    .set_global_opts(
        title_opts=opts.TitleOpts(title="游戏胜率"),
        xaxis_opts=opts.AxisOpts(type_="category")
    )
    .render("不同类别胜率.html")
)
os.system("不同类别胜率.html")
#用户游戏场次
sql = """
select 'PVP' as `游戏类型`,
       avg(pvp_battle_count) as `平均场次`,
       sum(case when pay_price > 0 then pvp_battle_count else 0 end) / sum(case when pay_price > 0 then 1 else 0 end) as `付费用户平均场次`,
       sum(case when pay_price = 0 then pvp_battle_count else 0 end) / sum(case when pay_price = 0 then 1 else 0 end) as `非付费用户平均场次`
from game_data
union all 
select 'PVE' as `游戏类型`,
       avg(pve_battle_count) as `均场次`,
       sum(case when pay_price > 0 then pve_battle_count else 0 end) / sum(case when pay_price > 0 then 1 else 0 end) as `付费用户平均场次`,
       sum(case when pay_price = 0 then pve_battle_count else 0 end) / sum(case when pay_price = 0 then 1 else 0 end) as `非付费用户平均场次`
from game_data
"""
data = pd.read_sql(con=engine,sql = sql)
c7 = (
    Bar()
    .add_dataset(
    source=[data.columns.tolist()] + data.values.tolist()
    )
    .add_yaxis(series_name="平均场次", y_axis=[])
    .add_yaxis(series_name="付费用户平均场次", y_axis=[])
    .add_yaxis(series_name="非付费用户平均场次", y_axis=[])
    .set_global_opts(
        title_opts=opts.TitleOpts(title="游戏场次"),
        xaxis_opts=opts.AxisOpts(type_="category"),
    )
    .render("用户游戏场次.html")
)
os.system("用户游戏场次.html")