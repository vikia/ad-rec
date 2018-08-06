# coding = utf-8
# author = wufeijia

from flask import Flask, request, json
import uuid
import hashlib
import random
import logging

app = Flask(__name__)
gdata = []

@app.route('/ad-rec', methods = ['POST', 'GET'])
def get_rec_by_uid():
    # params = request.get_json()
    app.logger.debug("request url params: %s", request)
    resp = {}
    uid = ''
    req_num = 0
    try:
        uid = request.args.get('uid')
        req_num = int(request.args.get('num'))

        # validate
        # verify = params['v']
        # c = "?uid=%s&salt=poc" % uid
        # if verify.lower() != hashlib.md5(c).hexdigest():
            # raise ValueError("Bad verify code")

        resp['uid'] = uid
        rnd_list = random.sample(range(len(gdata)), req_num)
        rec_list = []
        for i in range (0, req_num):
            rec_item = gdata[rnd_list[i]]
            rec_item['score'] = random.random()
            rec_item['strategy'] = 1
            rec_list.append(rec_item)
        resp['ad_res'] = rec_list
    except Exception as e:
        app.logger.warning("Bad request: %s", e)
        resp = {"error_code":1, "error":"invalid param"}

    result = json.jsonify(resp)
    app.logger.info("ip=%s uid=%s req_num=%d ad_res=%s", request.remote_addr, uid, req_num, resp)
    return result

def load_resouce(data_path):
    df = open(data_path, 'r')
    for line in df:
        try:
            infos = line.strip().split('\t')
            d = {'ad_id':int(infos[0]), 'ad_title':infos[1], 'ad_cate':infos[2], 'ad_img':infos[-1]}
            gdata.append(d)
        except Exception as e:
            app.logger.warning("Bad line format: %s", line)
            continue
    df.close()

if __name__ == '__main__':
    logging.basicConfig(filename="log/rec-serv.log", level="INFO", \
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # logging.setLevel('INFO')
    load_resouce('data/movies.all.txt')
    app.run(debug=False)
