# coding = utf-8
# author = wufeijia

from flask import Flask, request, json, render_template
import uuid
import hashlib
import random
import logging
import datetime

app = Flask(__name__)

g_materials_list = []
g_nn_rec_dict = {}
g_hot_rec_list = []

g_cache = {}
CACHE_TIME_OUT = 30 * 60
def set_cache(key, item):
    g_cache[key] = (item, datetime.datetime.now())

def get_cache(key):
    if not g_cache.has_key(key):
        return None
    item, start = g_cache[key]
    ds = (datetime.datetime.now() - start).seconds
    if ds > CACHE_TIME_OUT:
        g_cache.pop(key)
        return None
    return item

@app.route('/demo.html')
def serve_demo():
    return render_template('demo.html')

@app.route('/get-userids', methods = ['POST', 'GET'])
def get_old_user():
    app.logger.debug("request url params: %s", request)
    no_cache = request.args.get('cache', '').lower() == 'no'
    ip = str(request.remote_addr)

    result = ''
    if no_cache or get_cache(ip) is None:
        resp = {}
        old_users = g_nn_rec_dict.keys()
        rnd_list = random.sample(range(len(old_users)), min(10, len(old_users)))
        old_sample_users = [old_users[r] for r in rnd_list]
        resp['old'] = old_sample_users
        resp['new'] = [random.randrange(50000, 99999) for i in range(10)]
        app.logger.info("ip=%s route=/get-userids no_cache=%s res=%s", request.remote_addr, no_cache, resp)
        result = json.jsonify(resp)
        set_cache(ip, result)
        return result
    else:
        return get_cache(ip)

def rec_nn_model(n, uid):
    rec_list = g_nn_rec_dict[uid]
    return rec_list[:min(n, len(rec_list))]

def rec_hot(n):
    return g_hot_rec_list[:min(n, len(g_hot_rec_list))]

def rec_random(n):
    rec_list = []
    rnd_list = random.sample(range(len(g_materials_list)), min(n, len(g_materials_list)))
    for i in range (0, n): 
        rec_item = g_materials_list[rnd_list[i]]
        rec_item['score'] = str(random.random() * 5)
        rec_item['strategy'] = 'random'
        rec_list.append(rec_item)
    return rec_list

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
        rec_list = []
        if g_nn_rec_dict.has_key(int(uid)):
            # rec_list = g_nn_rec_dict[int(uid)]
            rec_list = rec_nn_model(req_num, int(uid))
            # resp['ad_res'] = rec_list[:req_num]
        else:
            hot_num = int(req_num * 0.6)
            rand_num = req_num - hot_num
            rec_list = rec_hot(hot_num) + rec_random(rand_num)
        resp['ad_res'] = rec_list
    except Exception as e:
        app.logger.warning("Bad request: %s", e)
        resp = {"error_code":1, "error":"invalid param"}

    result = json.jsonify(resp)
    app.logger.info("ip=%s route=/ad-rec uid=%s req_num=%d ad_res=%s", \
            request.remote_addr, uid, req_num, resp)
    return result

def load_materials(data_path):
    df = open(data_path, 'r')
    for line in df:
        try:
            infos = line.strip().split('\t')
            d = {'ad_id':int(infos[0]), 'ad_title':infos[-2], 'ad_cate':infos[2], 'ad_img':infos[-1]}
            g_materials_list.append(d)
        except Exception as e:
            app.logger.warning("Bad line format: %s", line)
            continue
    df.close()

def load_nn_rec_res(data_path):
    df = open(data_path, 'r')
    for line in df:
        try:
            uid, rec_json = line.strip().split('\t')
            g_nn_rec_dict[int(uid)] = json.loads(rec_json)
        except Exception as e:
            app.logger.warning("Bad line format: %s", line)
            continue
    df.close()

def load_hot_rec_res(data_path):
    df = open(data_path, 'r')
    for line in df:
        try:
            cnt, rec_json = line.strip().split('\t')
            g_hot_rec_list.append(json.loads(rec_json))
        except Exception as e:
            app.logger.warning("Bad line format: %s", line)
            continue
    df.close()

if __name__ == '__main__':
    logging.basicConfig(filename="log/rec-serv.log", level="INFO", \
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # logging.setLevel('INFO')
    load_materials('data/movies.all.txt')
    load_nn_rec_res('./data/nn_rec.res.txt')
    load_hot_rec_res('./data/hot_movies.txt')
    app.run(debug=False, port=3389, host='0.0.0.0')
