from cache import channelsCache
from flask import Blueprint, current_app, jsonify, render_template

bp = Blueprint("clubhouse", __name__)


@bp.route("/")
def index():
    return render_template("index.html", owner_user_id=current_app.config['OWNER_USER_ID'])


@bp.route("/api/getChannels")
def getChannels():
    rooms, channels = channelsCache.get()
    current_app.logger.info(f"len of channels = {len(channels)}")
    return jsonify(channels)


@bp.route("/room/<string:room>")
def join(room):
    return render_template("channel.html", owner_user_id=current_app.config['OWNER_USER_ID'])


@bp.route("/api/room/<string:room>")
def getChannel(room):
    rooms, channels = channelsCache.get()
    if room in rooms and rooms[room]['channel']['joined'] is True:
        return rooms[room]
    return jsonify(None)


# @bp.route("/test")
# def test():
#     return render_template("channel.html", owner_user_id=current_app.config['OWNER_USER_ID'])
from hashlib import sha256
from datetime import datetime
import json


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self,obj)

class BlockChain:
    def __init__(self):

        #saved by list
        self.Chain=[]
        #storing current tranactions
        #updated after creating new block
        self.TransactionPool=[]
        self.Difficulty=3

        #first block initialized
        nonce=0
        firstblock={
            "Index":len(self.Chain)+1,
            "PreHash": None,
            "Timestamp":datetime.now(),
            "Transactions": self.TransactionPool,
            "Nonce":nonce
        }
        testhash=self.Get_BlockHash(firstblock)
        while self.Is_ValidDifficulty(testhash) is False:
            nonce+=1
            testhash=self.Get_Hash(firstblock,nonce)
        self.Add_NewBlock(firstblock)

    def Change_Difficulty(self,NewDifficulty):

        self.Difficulty=NewDifficulty

    def Is_ValidDifficulty(self,TestHash):

        if TestHash[:self.Difficulty]=="0"*self.Difficulty:
            return True
        return False

    def Get_BlockHash(self,Block):

        block_str=json.dumps(Block,sort_keys=True,cls=DateEncoder).encode("utf-8")
        return sha256(block_str).hexdigest()

    def Get_Hash(self,TestBlock,NewNonce):

        TestBlock["Timestamp"]=datetime.now()
        TestBlock["Nonce"]=NewNonce
        return self.Get_BlockHash(TestBlock)

    def Add_NewBlock(self,NewBlock):

        if self.Is_ValidDifficulty(self.Get_BlockHash(NewBlock)):
            self.Chain.append(NewBlock)
            self.TransactionPool=[]
            return True
        return False

    def Creat_NewBlock(self):

        nonce=0
        newblock = {
            "Index":len(self.Chain)+1,
            "PreHash": self.Get_BlockHash(self.Chain[-1]),
            "Timestamp": datetime.now(),
            "Transactions": self.TransactionPool,
            "Nonce": nonce
        }
        testhash = self.Get_BlockHash(newblock)
        while self.Is_ValidDifficulty(testhash) is False:
            nonce += 1
            testhash = self.Get_Hash(newblock, nonce)

        return newblock

    def Is_ValidChain(self,Chain):

        lastblock=Chain[0]
        currentindex=1

        while currentindex<len(Chain):
            block=Chain[currentindex]
            if block["PreHash"]!=self.Get_BlockHash(lastblock):
                return False
            if not self.Is_ValidDifficulty(self.Get_BlockHash(block)):
                return False
            lastblock=block
            currentindex+=1
        return True

    def Add_NewTransaction(self,Sender,Receiver,Amount):
        transaction={
            "Sender": Sender,
            "Receiver": Receiver,
            "Amount": Amount,
        }
        self.TransactionPool.append(transaction)




print("op")

blockchain=BlockChain()

blockchain.Add_NewTransaction("Jason","Bob",114514)

blockchain.Add_NewBlock(blockchain.Creat_NewBlock())

print(blockchain.Chain[-1])
print(blockchain.Is_ValidChain(blockchain.Chain))
