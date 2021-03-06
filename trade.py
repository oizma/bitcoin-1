from train import *

import pickle as pkl

def test_trading(data, clusters):
    # iterate over test data,
    # making decisions at each time step

    holdings_usd = 100000
    holdings_btc = 0

    holdings_usd_start = holdings_usd

    seq = lambda n: [x[1] for x in data[i-n:i]]
    for i in range(720, len(data)-1):
        p1 = predict(seq(180), clusters[0])
        p2 = predict(seq(360), clusters[1])
        p3 = predict(seq(720), clusters[2])
        ask = data[i][2]
        bid = data[i][3]
        r = (bid-ask)/(bid+ask)

        pred = weights[0] + weights[1]*p1 + weights[2]*p2 + weights[3]*p3 + weights[4]*r

        if (pred > 0.000001 and holdings_usd>=data[i]):
            print("BUY")
            holdings_usd-=data[i]
            holdings_btc+=1
        elif (pred < -0.000001 and holdings_btc >= 1):
            print("SELL")
            holdings_usd+=data[i]
            holdings_btc-=1
        else:
            print("hold")

    holdings_usd += data[-1] * holdings_btc

    print str(holdings_usd / holdings_usd_start)+"% return"


# Test the model
if __name__=="__main__":
    if (len(sys.argv)) == 1:
        print "Need csv with testing data"
        quit()

    # load dataset, convert to 10s time increments
    data = load(sys.argv[1])[::2]

    # load clusters and weights
    try:
        clusters = pkl.load(open("weights/clusters.pkl", "rb"))
        weights = pkl.load(open("weights/weights.pkl", "rb"))
        #weights = [0.02085571, -1.1125847, 0.09749599, -1.56908484, 0.00331902]
        #weights = [-0.00570016, -0.2617486, -0.63571931, 0.13415341, 0.00337089]
    except:
        print "Generate weights and clusters with train.py"
        quit()

    test_trading(data,clusters)
