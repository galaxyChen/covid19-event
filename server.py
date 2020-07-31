from flask import Flask
from flask import request
from flask import jsonify
import json
import time

app = Flask(__name__)


def get_news(date):
    return date+"""
    出现第一位武汉市民有不明原因肺炎症状（事后确诊，当时未知是不明原因肺炎，且尚无医生发现和报告）。据金银潭医院的重症监护病房（ICU）主任吴文娟透露，该病患是一名年过七旬的男子，有点脑梗、老年痴呆。发病后，先被送入武汉市的另一家医院，但随着病情恶化，12月29日被转入金银潭医院。这名老人住在离海鲜市场四五站（公交站）远的地方，由于此前便患病在家，基本上不出门，并没有前往过华南海鲜市场。12月1日这个发病时间是通过流行病学调查综合家属回忆得出的结论。见Chaolin Huang, et al. Clinical features of patients infected with 2019 novel coronavirus in Wuhan, China. The Lancet, Jan. 24, 2020（中国武汉地区2019年新型冠状病毒感染者的临床特征）以及BBC中文 · 肺炎疫情：模糊不清的“零号病人”与病毒来源争议。
【按，注意出现病症、入院、确诊“不明原因（病毒性）肺炎”、确诊“新冠肺炎”、确定有限人传人、确定持续人传人的区别。本时间线注重信息（概念提出）时间的记录。】
"""

def get_next_date(date):
    date = date.split('-')
    date = [int(t) for t in date]
    date[-1] += 1
    if date[-1] > 31:
        date[-1] = 1
        date[-2] += 1
    if date[-2] > 12:
        date[0] += 1
    date = [str(t) for t in date]
    return '-'.join(date)


@app.route('/getNews', methods=['GET'])
def getNews():
    begin = request.args.get('begin')
    end = request.args.get('end')
    begin = begin.split('-')
    begin = int(begin[-1])
    end = end.split('-')
    end = int(end[-1])

    dates = []
    date = request.args.get('begin')
    for i in range(abs(begin-end)+1):
        dates.append(date)
        date = get_next_date(date)
    news = [get_news(date) for date in dates]
    pics = ['']*len(news)
    return jsonify({
        'dates': dates,
        'news': news,
        'pics': pics
    })


@app.route('/getOneNews', methods=['GET'])
def getOneNews():
    date = request.args.get('date')

    news = get_news(date)
    url = ""
    return jsonify({
        'date': date,
        'news': news,
        'pic': ""
    })
