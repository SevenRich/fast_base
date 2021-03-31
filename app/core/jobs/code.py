from app.core.crud import crud_order
import time
import random
import json
import os.path

from hashids import Hashids
from sqlalchemy import text

from ...config import settings
from ...utils.logger import logger
from ...utils.codetool import CodeTool
from ...core import crud
from ...utils.deps import get_db
from ...models.codes import get_model, create_table
from ...models.code import Code


def generator_standard_code(db, config):
    import time
    # time.sleep(30)
    print('======================== 开始生码 =========================')
    print(config.__dict__)
    print('======================== 参数获取 =========================')
    
    # print('code_sn:', config.code_sn)
    # print('company_code:', config.company_code)
    # print('code_type:', config.code_type)
    # print('relevance_type:', config.relevance_type)
    # print('counts:', config.counts)
    # print('export_key:', config.export_key)
    # print('url_prefix:', config.url_prefix)
    # print('batch_sn:', config.batch_sn)
    # print('code_config:', config.code_config)
    # code_config = json.loads(config.code_config)
    # print(type(code_config))
    # print('export_config.big_code:', code_config['big_code'])
    # print('export_config.middle_code:', code_config['middle_code'])
    # print('export_config:', config.export_config)
    # export_config = json.loads(config.export_config)
    # print(type(export_config))
    # print('export_config.url_format:', export_config['url_format'])
    # print('export_config.export_query:', export_config['export_query'])
    
    
    if config.status not in [0, 3]:
        # 状态为 0 等待 3 取消
        logger.error('重复生码请求!')
        print('重复生码请求!')
        return 
    
    # # 有锁文件
    # lock_path = settings.BASE_PATH + '/runtime/locks/' + str(config.code_sn)
    # if os.path.exists(lock_path):
    #     logger.error('生码已经在执行中!')
    #     print('生码已经在执行中!')
    #     return 
    
    # 开始生码
    try:
        order_info = crud.order.get(db, id=config.id)
        if order_info is None:
            print('code order is not exist!')
            logger.error('code order is not exist!')
            raise Exception('code order is not exist!') 
        
        # # 添加锁文件
        # file = open(lock_path, 'w')
        # file.close()
        
        # 开始生码
        # 获取商户信息 码表是否已经存在
        company = crud.company.get_by_code(db, code=config.company_code)
        if company is None:
            print('Company is not exist!')
            logger.error('Company is not exist!')
            raise Exception('Company is not exist!') 
        # suffix
        suffix = company.uuid_code
        # 码表是否已经存在
        # create_table(suffix)
        # 获取码类
        code_model = get_model(suffix)
        
        if config.relevance_type == 1 and config.code_type == 1:
            # 前关联 标准码
            relevance_standard(db=db, code_model=code_model, config=config)
        
        if config.relevance_type == 1 and config.code_type == 2:
            # 前关联 套码
            pass
        
    except Exception:
        # 异常
        # 更新生码状态 为 3 取消
        form_data = dict()
        form_data['status'] = 3
        crud.order.update(db, db_obj=order_info, obj_in=form_data)
        
    else:
        # 如果没有异常发生
        # 更新生码状态 2 完成 done
        form_data = dict()
        form_data['status'] = 3
        crud.order.update(db, db_obj=order_info, obj_in=form_data)
        
    # # 删除锁文件
    # if os.path.exists(lock_path): # 如果文件存在
    #     #删除文件
    #     os.remove(lock_path)
    
    # print(CodeTool.create_random_number(6))
    # print(CodeTool.create_serial_number(455664, 8))
    # a = set()
    # [a.add(CodeTool.create_random_str(12)) for i in range(100000)]
    # print(len(a))
    # print(CodeTool.create_hashids_str(number=12345678901234567890, min_length=12))

    print('======================== 结束生码 =========================')
    
def relevance_standard(db, code_model, config):
    # 标准码 
    code_config = json.loads(config.code_config)
    
    # 判断 code_config 三个参数 小码、 防伪码 、 验证码
    
    # 生码规则配置:
    # code_type 1 全数字 2 全字母 3 数字字母
    # type 1 数字码随机数字  2 数字码顺序流水号 3 乱码
    if code_config['small_code']['status'] == 1:
        small_code = create_code_by_big_mid_small(db=db, code_model=code_model, config=config, type='small_code')
        
    if code_config['security_code']['status'] == 1:
        security_code = create_code_by_big_mid_small(db=db, code_model=code_model, config=config, type='security_code')
        
    if code_config['verify_code']['status'] == 1:
        verify_code = create_code_by_big_mid_small(db=db, code_model=code_model, config=config, type='verify_code')
    
    # 合成需要的数据，并写入数据库
    

def relevance_group():
    pass

def create_code_by_big_mid_small(db, code_model, config, type='big_code'):
    batch_sn = config.batch_sn
    code_config = json.loads(config.code_config)
    codes = set()
    print(int(config.counts))
    while len(codes) < int(config.counts):
        # 生码规则配置:
        #     # code_type 1 全数字 2 全字母 3 数字字母
        #     # type 1 数字码随机数字  2 数字码顺序流水号 3 乱码
        # 生一个码
        if code_config[type]['type'] in [1, 2] and code_config[type]['code_type'] == 1:
            code_item = CodeTool.create_random_number(length=code_config[type]['length']);
            
        if code_config[type]['type'] == 3 and code_config[type]['code_type'] == 2:
            code_item = CodeTool.create_random_str(base_str='ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz' , length=code_config[type]['length']);
            
        if code_config[type]['type'] == 3 and code_config[type]['code_type'] == 3:
            code_item = CodeTool.create_random_str(code_config[type]['length']);
        
        print(code_item)
        
        if type == 'big_code':
            if db.query(code_model).filter_by(batch_sn=batch_sn, big_code=code_item).all() is None:
                codes.add(code_item)
                continue
        if type == 'middle_code':
            if db.query(code_model).filter_by(batch_sn=batch_sn, middle_code=code_item).all() is None:
                codes.add(code_item)
                continue
        if type == 'small_code':
            print(codes, 1000000)
            print(len(codes), 200000)
            ret = db.execute(text('select * from :table'), params={'table':code_model.__tablename__}).first()
            print(ret)
            try:
                if db.query(code_model).filter(code_model.batch_sn == batch_sn, code_model.small_code == code_item).all():
                    print(codes, 3000000)
                    codes.add(code_item)
                    print(len(codes))
            except Exception:
                raise Exception
                print(codes, 4000000)
            else:
                print(codes, 5000000)
                
        if type == 'security_code':
            if db.query(code_model).filter_by(batch_sn=batch_sn, security_code=code_item).all() is None:
                codes.add(code_item)
                continue
            
        if type == 'verify_code':
            codes.add(code_item)
            continue

    print(codes)
    print(len(codes))
    return codes
