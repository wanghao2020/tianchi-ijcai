class evaluation:
    S_true = {}
    S_predict = {}
    Budget = {}
    def getS_true(self,testdata):
        with open(testdata) as f:
            for line in f:
                line = line.strip('\r\n')
                user,merchant,location,time = line.split(',')
                UML_pair = (user,merchant,location)
                if not self.S_true.has_key(merchant):
                    self.S_true[merchant] = []
                if UML_pair not in self.S_true[merchant]:
                    self.S_true[merchant].append(UML_pair)

    def getS_predict(self,resultdata):
        with open(resultdata) as f:
            for line in f:
                line = line.strip('\r\n')
                user,location,merchantlist = line.split(',')
                merchants = merchantlist.split(':')
                for mer in merchants:
                   UML_pair = (user,mer,location)
                   if not self.S_predict.has_key(mer):
                       self.S_predict[mer] = []
                   if UML_pair not in self.S_predict[mer]:
                       self.S_predict[mer].append(UML_pair)

    def get_MerchantBudget(self,merchantdata):
        with open(merchantdata) as f:
            for line in f:
                line = line.strip('\r\n')
                merchant,budget,location = line.split(',')
                self.Budget[merchant] = budget

    def comp_f1_score(self):
        P_down = 0
        R_down = 0
        up = 0
        for merchant in self.Budget:
            right_num = len(set(self.S_predict[merchant]) & set(self.S_true[merchant]))
            up += min(right_num,self.Budget[merchant])
            P_down += len(set(self.S_predict[merchant]))
            R_down += min(len(set(self.S_true[merchant])),self.Budget[merchant])
        P = float(up)/P_down
        R = float(up)/R_down
        F1_score = 2*P*R/(P+R)
