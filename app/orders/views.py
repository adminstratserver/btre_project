from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from .models import Order
from .permissions import IsOwnerOrReadOnly, IsAuthenticated
from .serializers import OrderSerializer
from .pagination import CustomPagination
# from .tasks import *
from celery.decorators import task
from ib_insync import *
import time
import random

class get_delete_update_order(RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

    def get_queryset(self, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            content = {
                'status': 'Not Found'
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        return order

    # Get a order
    def get(self, request, pk):

        order = self.get_queryset(pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Update a order
    def put(self, request, pk):

        order = self.get_queryset(pk)

        if (request.user == order.creator):  # If creator is who makes request
            serializer = OrderSerializer(order, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            content = {
                'status': 'UNAUTHORIZED'
            }
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)

    # Delete a order
    def delete(self, request, pk):

        order = self.get_queryset(pk)

        if (request.user == order.creator):  # If creator is who makes request
            order.delete()
            content = {
                'status': 'NO CONTENT'
            }
            return Response(content, status=status.HTTP_204_NO_CONTENT)
        else:
            content = {
                'status': 'UNAUTHORIZED'
            }
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)


class get_post_orders(ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    def get_queryset(self):
        orders = Order.objects.all()
        return orders

    # Get all orders
    def get(self, request):
        orders = self.get_queryset()
        paginate_queryset = self.paginate_queryset(orders)
        serializer = self.serializer_class(paginate_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    # Create a new order
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user)

            msg_tradeorder = request.data["tradeorder"]
            msg_datetime = request.data["datetime"]
            msg_sequencenumber = request.data["sequencenumber"]
            test_message.delay(msg_tradeorder, msg_datetime, msg_sequencenumber)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@task(name="test_message")
def test_message(msg_tradeorder, msg_datetime, msg_sequencenumber):

    TWS_IP_Address = '157.245.201.86'

    SSF_Reserved_Capital= 10000 #this value is supposed to be extracted from subscriber's MySQL database via Python Web Services
    Subscriber_Reserved_Capital= 10000 #this value is supposed to be extracted from SSF's MySQL database via Python Web Services
    Global_QtyPerLeg = int(Subscriber_Reserved_Capital / SSF_Reserved_Capital)

    #print('Global_QtyPerLeg=',Global_QtyPerLeg)
    #print("Test 2: clientinput = ", clientinput)
    #clientinput = input("1. Enter input = ")

    #incomingdata = "ADD[('SPX','20191115','P2810/P2820/P2830/P2840','1')]CUR[]"
    print('01. msg_tradeorder = ', msg_tradeorder)
    incomingdata = msg_tradeorder
    print('02. msg_datetime = ', msg_datetime)
    print('03. msg_sequencenumber = ', msg_sequencenumber)
    incomingCUR = incomingdata[str(incomingdata).find("CUR[") + 4:str(incomingdata).find("]",str(incomingdata).find("CUR[") + 4)]
    #print('At True: incomingCUR=',incomingCUR)
    checkPos = checkPositions(incomingCUR, TWS_IP_Address)

    print('checkPos=',checkPos)
    if checkPos=='Y':
        if str(incomingdata).count("ADD")>0:
            openComboPosition(TWS_IP_Address, incomingdata)
        if str(incomingdata).count("MOD")>0:
            openComboPosition(TWS_IP_Address, incomingdata)

    t2 = time.time()
    time.sleep(1) #
    t3 = time.time()
    print('Total sleep time: %.2f ms' % (t3 - t2))
    #await asyncio.sleep(0.01)
    #IB.sleep(1)



def Removedup102(ttlNew1):

    ttlNew2 = ttlNew1
    #print('1. ttlNew2=', ttlNew2)

    for i in range(len(ttlNew1)):
        for j in range(i + 1, len(ttlNew1)):
            checkmatch1 = set(ttlNew1[i][:5]) & set(ttlNew1[j][:5])
            # print('1. compare = %s %s checkmatch1 = %d' % (ttlNew1[i], ttlNew1[j], len(checkmatch1)))
            if len(checkmatch1) == 5:
                # print('2. compare = %s %s checkmatch1 = %d' % (ttlNew1[i], ttlNew1[j], len(checkmatch1)))
                # print ('2. qty = %d %d' % (ttlNew1[i][5], ttlNew1[j][5]))
                ttlNew2[i][5] = ttlNew1[i][5] + ttlNew1[j][5]

    #print('2. ttlNew2=', ttlNew2)

    final_list = []
    final_list.append(ttlNew1[0])
    # print('1. final_list=%s'% (final_list[-1]))
    x = 0
    y = 0
    matched = "N"
    for num in ttlNew1:
        # print('1. final_list=%s'% (final_list[x]))
        # print('START:num=%s'% (num))
        # print ('len(final_list)=',len(final_list))
        for x in range(0, len(final_list)):
            # print('1. num[:5]=%s final_list=%s'% (num[:5],final_list))
            imatch = set(final_list[x]) & set(num[:5])
            # print('3. imatch',imatch)
            # print('1. len(imatch)=',len(imatch))
            if len(imatch) == 5:
                # print ('DO NOT COPY')
                matched = "Y"

        if matched == "N":
            x = x + 1
            # print('-->1. final_list=',final_list)
            # print('-->1. duplicate[y]',duplicate[y])
            final_list.append(ttlNew1[y])

        matched = "N"
        # print('-->2. final_list=',final_list)
        # print('')
        y = y + 1

    return final_list

def Removedup101(ttlNew1):

    ttlNew2 = ttlNew1
    #print('1. ttlNew2=', ttlNew2)

    for i in range(len(ttlNew1)):
        for j in range(i + 1, len(ttlNew1)):
            checkmatch1 = set(ttlNew1[i][:4]) & set(ttlNew1[j][:4])
            # print('1. compare = %s %s checkmatch1 = %d' % (ttlNew1[i], ttlNew1[j], len(checkmatch1)))
            if len(checkmatch1) == 4:
                # print('2. compare = %s %s checkmatch1 = %d' % (ttlNew1[i], ttlNew1[j], len(checkmatch1)))
                # print ('2. qty = %d %d' % (ttlNew1[i][4], ttlNew1[j][4]))
                ttlNew2[i][4] = ttlNew1[i][4] + ttlNew1[j][4]

    #print('2. ttlNew2=', ttlNew2)

    final_list = []
    final_list.append(ttlNew1[0])
    # print('1. final_list=%s'% (final_list[-1]))
    x = 0
    y = 0
    matched = "N"
    for num in ttlNew1:
        # print('1. final_list=%s'% (final_list[x]))
        # print('START:num=%s'% (num))
        # print ('len(final_list)=',len(final_list))
        for x in range(0, len(final_list)):
            # print('1. num[:4]=%s final_list=%s'% (num[:4],final_list))
            imatch = set(final_list[x]) & set(num[:4])
            # print('3. imatch',imatch)
            # print('1. len(imatch)=',len(imatch))
            if len(imatch) == 4:
                # print ('DO NOT COPY')
                matched = "Y"

        if matched == "N":
            x = x + 1
            # print('-->1. final_list=',final_list)
            # print('-->1. duplicate[y]',duplicate[y])
            final_list.append(ttlNew1[y])

        matched = "N"
        # print('-->2. final_list=',final_list)
        # print('')
        y = y + 1

    return final_list

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

def commitPosition(TWS_IP_Address, optLegs, BuySell):   #The quantity is dependent on the Global_QtyPerLeg

    Global_QtyPerLeg = 1
    #print('At commitPosition:')
    ib = IB()
    #print('11. ib=', ib)
    t0 = time.time()
    id1 = random.randint(1,201)
    ib.connect(TWS_IP_Address, 7496, clientId=id1)
    print('Open Connection clientid %d = %s ' % (id1, ib))
    conid = []

    #print('->1. optLegs=%s BuySell=%s' % (optLegs, BuySell))
    numlegs1 = len(optLegs)
    #print('numlegs1=',numlegs1)

    qty1 = abs(int(optLegs[0][5]))
    #print('->2. qty1=',qty1)

    for x in range (numlegs1):
        optLegs[x][5] = abs(int(optLegs[x][5] / qty1))

    for x in range(0, numlegs1):

        '''
        print('1. Element %d. = %s' % (x, optLegs[x][0]))
        print('2. Element %d. = %s' % (x, optLegs[x][1]))
        print('3. Element %d. = %s' % (x, optLegs[x][2]))
        print('4. Element %d. = %s' % (x, optLegs[x][3]))
        print('5. Element %d. = %s' % (x, optLegs[x][4]))
        print('6. Element %d. = %s' % (x, optLegs[x][5])) #ratio
        '''

        leg1 = Option(optLegs[x][0], int(optLegs[x][1]), optLegs[x][2], optLegs[x][3], 'SMART')
        ##print ('%d. leg1= %s' % (x,leg1))
        ib.qualifyContracts(leg1)
        conid.append(leg1.conId)
        #print("leg1 [%d] = %s" % (x, leg1))
        ##print("conid[%d] = %s" % (x,conid[x]))
        # ib.qualifyContracts(Opt_front,Opt_back)

    #print('numlegs1=', numlegs1)
    if numlegs1==1:
        contract1 = Option(optLegs[0][0], optLegs[0][1], int(optLegs[0][2]), optLegs[0][3], 'SMART')

    elif numlegs1==2:
        contract1 = Contract(symbol='SPX', secType='BAG', exchange='SMART', currency='USD',
                             comboLegs=[ComboLeg(conId=conid[0], ratio=optLegs[0][5], action=optLegs[0][4]),
                                        ComboLeg(conId=conid[1], ratio=optLegs[1][5], action=optLegs[1][4])])

    elif numlegs1 == 3:
        contract1 = Contract(symbol='SPX', secType='BAG', exchange='SMART', currency='USD',
                             comboLegs=[ComboLeg(conId=conid[0], ratio=optLegs[0][5], action=optLegs[0][4]),
                                        ComboLeg(conId=conid[1], ratio=optLegs[1][5], action=optLegs[1][4]),
                                        ComboLeg(conId=conid[2], ratio=optLegs[2][5], action=optLegs[2][4])])

    elif numlegs1 == 4:
        contract1 = Contract(symbol='SPX', secType='BAG', exchange='SMART', currency='USD',
                             comboLegs=[ComboLeg(conId=conid[0], ratio=optLegs[0][5], action=optLegs[0][4]),
                                        ComboLeg(conId=conid[1], ratio=optLegs[1][5], action=optLegs[1][4]),
                                        ComboLeg(conId=conid[2], ratio=optLegs[2][5], action=optLegs[2][4]),
                                        ComboLeg(conId=conid[3], ratio=optLegs[3][5], action=optLegs[3][4])])

    # ib.qualifyContracts(contract)  #qualifyContracts cannot be used for ComboLegs

    order1 = MarketOrder(BuySell, Global_QtyPerLeg*qty1)         # market order
    ##print ('order1 =', order1)
    #order1 = LimitOrder('BUY', 1, 1.90)  # limit order, limit price at the end

    '''
    print('2. BuySell=', BuySell)
    print('2. qty1=', qty1)
    print('2. Global_QtyPerLeg=', Global_QtyPerLeg)
    print('2. Total Final Qty=', Global_QtyPerLeg * qty1)
    print('2. optLegs=', optLegs)
    '''
    #david007
    ##print('contract1 =',contract1)
    ib.placeOrder(contract1, order1)
    #print('Contract Order=',contract1)
    ##print('Place Order =', order1)
    ib.disconnect()
    print('Closed Connection')
    #IB.waitOnUpdate(timeout=0.1)
    t1 = time.time()
    print('Total time: %.2f ms' % (t1-t0))

def openComboPosition(TWS_IP_Address, incomingdata):
    #print('At openComboPosition:')
    pos2 = 0
    #print('6. incomingdata=', incomingdata)

    if incomingdata.count("ADD") > 0:
        incomingADD = incomingdata[str(incomingdata).find("ADD[") + 4:str(incomingdata).find("]", str(incomingdata).find("ADD[") + 4)]
        numberADD = incomingADD.count("(")
        #print('incomingADD=', incomingADD)
        #print('numberADD=',numberADD)
        for x in range(numberADD):
            optionleg2 = []

            pos1 = str(incomingADD).find("(", pos2)
            pos2 = str(incomingADD).find(")", pos1)
            incomingADD1 = eval('[' + incomingADD[pos1 + 1:pos2] + ']')
            #print('incomingADD1 = %s' % (incomingADD1))

            if incomingADD1[2].count("/") == 3:
                poss1 = incomingADD1[2].find('/')
                poss2 = incomingADD1[2].find('/', poss1 + 1)
                poss3 = incomingADD1[2].find('/', poss2 + 1)
                if poss1 != 0:                                         # 1st leg
                    optionleg2.append([incomingADD1[0], incomingADD1[1], incomingADD1[2][1:poss1], incomingADD1[2][:1], 'BUY', int(incomingADD1[3])])
                if poss2 - poss1 != 1:                                 # 2nd leg
                    optionleg2.append([incomingADD1[0], incomingADD1[1], incomingADD1[2][poss1 + 2:poss2], incomingADD1[2][poss1 + 1:poss1 + 2], 'SELL', int(incomingADD1[3])*-1])
                if poss3 - poss2 != 1:                                 # 3rd leg
                    optionleg2.append([incomingADD1[0], incomingADD1[1], incomingADD1[2][poss2 + 2:poss3], incomingADD1[2][poss2 + 1:poss2 + 2], 'SELL', int(incomingADD1[3])*-1])
                if poss3 != len(incomingADD1[2]) - 1:                  # 4th leg
                    optionleg2.append([incomingADD1[0], incomingADD1[1], incomingADD1[2][poss3 + 2:], incomingADD1[2][poss3 + 1:poss3 + 2], 'BUY', int(incomingADD1[3])])
                #print('optionleg2=', optionleg2)

            if incomingADD1[2].count("/") == 2:  # 3 legs
                print("Error! 2 slash is not allowed!")

            elif incomingADD1[2].count("/") == 1:  # 1 or 2 legs

                poss1 = incomingADD1[2].find('/')
                if poss1 != 0:  # 2 legs
                    poss1 = incomingADD1[2].find('/')
                    optionleg2.append([incomingADD1[0], incomingADD1[1], incomingADD1[2][1:poss1], incomingADD1[2][:1], 'BUY', int(incomingADD1[3])])
                    optionleg2.append([incomingADD1[0], incomingADD1[1], incomingADD1[2][poss1 + 2:], incomingADD1[2][poss1 + 1:poss1 + 2], 'SELL', int(incomingADD1[3]) * -1])

                elif poss1 == 0:  # 1 leg
                    optionleg2.append([incomingADD1[0], incomingADD1[1], incomingADD1[2][2:], incomingADD1[2][1:2], 'SELL',int(incomingADD1[3])*-1])

            elif incomingADD1[2].count("/") == 0:  # 1 leg
                optionleg2.append([incomingADD1[0], incomingADD1[1], incomingADD1[2][1:], incomingADD1[2][:1], 'BUY', int(incomingADD1[3])])

            #print('->>2.  optionleg2=', optionleg2)
            optionleg5 = Removedup102(optionleg2)
            if incomingADD1[2].count("/") == 1 and poss1==0:
                buysell1 = 'SELL'
            else:
                buysell1 = 'BUY'
            #print('optionleg5=%s buysell1=%s' % (optionleg5, buysell1))
            commitPosition(TWS_IP_Address, optionleg5, buysell1)

    else:
        print('No incoming ADD')

    if incomingdata.count("MOD") > 0:
        incomingMOD = incomingdata[str(incomingdata).find("MOD[") + 4:str(incomingdata).find("]", str(incomingdata).find("MOD[") + 4)]
        numberMOD = incomingMOD.count("(")
        #print('1. incomingMOD=', incomingMOD)
        #print('2. numberMOD=',numberMOD[3])
        for x in range(numberMOD):

            optionleg2 = []

            pos1 = str(incomingMOD).find("(", pos2)
            pos2 = str(incomingMOD).find(")", pos1)
            incomingMOD1 = eval('[' + incomingMOD[pos1 + 1:pos2] + ']')
            print('2. incomingMOD1=', incomingMOD1)
            print('3. incomingMOD1[3]=', incomingMOD1[3])
            #david007
            print('len(Global_NormalisedCurr)=',len(Global_NormalisedCurr))

            leg1BS = 'BUY'
            leg2BS = 'SELL'
            leg3BS = 'SELL'
            leg4BS = 'BUY'

            for x in range(len(Global_NormalisedCurr)):

                icount2 = set(Global_NormalisedCurr[x]) & set(incomingMOD1)
                print('')
                print('1. Global_NormalisedCurr[%d]=%s' % (x, Global_NormalisedCurr[x]))
                print('2. incomingMOD1=%s' % (incomingMOD1))
                print('3. len(icount2)=%d' % (len(icount2)))
                print('')

                if len(icount2) == 3:
                   qtyNCurr1 = Global_NormalisedCurr[x][3]
                   qtyNMod1 = incomingMOD1[3]
                   #print('1. qtyNCurr1=',qtyNCurr1)
                   #print('1. qtyNMod1=', qtyNMod1)
                   qtyChange= abs(int(qtyNMod1) - int(qtyNCurr1))

            countslash = incomingMOD1[2].count("/")
            poss1 = incomingMOD1[2].find('/')
            poss2 = incomingMOD1[2].find('/', poss1 + 1)
            poss3 = incomingMOD1[2].find('/', poss2 + 1)

            if poss1 == 0 and countslash ==1:
                onelegonestash = True
            else:
                onelegonestash = False

            if countslash == 3:

                if poss1 != 0:
                    optionleg2.append([incomingMOD1[0], incomingMOD1[1], incomingMOD1[2][1:poss1], incomingMOD1[2][:1], leg1BS, qtyChange])

                if poss2 - poss1 != 1:
                    optionleg2.append([incomingMOD1[0], incomingMOD1[1], incomingMOD1[2][poss1 + 2:poss2], incomingMOD1[2][poss1 + 1:poss1 + 2], leg2BS, qtyChange])

                if poss3 - poss2 != 1:
                    optionleg2.append([incomingMOD1[0], incomingMOD1[1], incomingMOD1[2][poss2 + 2:poss3], incomingMOD1[2][poss2 + 1:poss2 + 2], leg3BS, qtyChange])

                if poss3 != len(incomingMOD1[2]) - 1:  # there is a 4th leg
                    optionleg2.append([incomingMOD1[0], incomingMOD1[1], incomingMOD1[2][poss3 + 2:], incomingMOD1[2][poss3 + 1:poss3 + 2], leg4BS, qtyChange])

            if countslash == 2:
                print("Error! 2 slash is not allowed!")

            elif countslash == 1:  # 1 or 2 legs

                if poss1 != 0:  # 2 legs - vertical

                    optionleg2.append([incomingMOD1[0], incomingMOD1[1], incomingMOD1[2][1:countslash], incomingMOD1[2][:1], leg1BS, qtyChange])
                    optionleg2.append([incomingMOD1[0], incomingMOD1[1], incomingMOD1[2][countslash + 2:],incomingMOD1[2][countslash + 1:countslash + 2], leg2BS, qtyChange])

                elif poss1 == 0:  # 1 leg and 1 slash - short

                    print('incomingMOD1=',incomingMOD1)
                    optionleg2.append([incomingMOD1[0], incomingMOD1[1], incomingMOD1[2][2:], incomingMOD1[2][1:2], leg2BS, qtyChange * -1])

            elif countslash == 0:  # 1 leg and no slash - long

                    optionleg2.append([incomingMOD1[0], incomingMOD1[1], incomingMOD1[2][1:], incomingMOD1[2][:1], leg2BS, qtyChange])

            optionleg8 = []
            print('2. optionleg2=', optionleg2)
            optionleg8 = Removedup102(optionleg2)
            #print('5. Global_Optionleg=', Global_Optionleg)
            print('2. qtyNCurr1=', qtyNCurr1)
            print('2. qtyNMod1=', qtyNMod1)
            print('2. optionleg8=', optionleg8)
            print('2. Global_NormalisedCurr=', Global_NormalisedCurr)

            if int(qtyNMod1) > int(qtyNCurr1):
                print('Increase because current qty is %s and new qty is %s' % (qtyNCurr1, qtyNMod1))
                if onelegonestash == True:
                    commitPosition(TWS_IP_Address, optionleg8,'SELL')
                else:
                    commitPosition(TWS_IP_Address, optionleg8, 'BUY')
            elif int(qtyNCurr1) > int(qtyNMod1):
                print('Reduce because current qty is %s and new qty is %s' % (qtyNCurr1, qtyNMod1))
                if onelegonestash == True:
                    commitPosition(TWS_IP_Address, optionleg8, 'BUY')
                else:
                    commitPosition(TWS_IP_Address, optionleg8, 'SELL')

    else:
        print('')
        #print('No MODIFICATION QTY commands')



def checkPositions(incomingCUR2, TWS_IP_Address):

  global Global_Optionleg
  global Global_NormalisedCurr
  Global_Optionleg = []
  Global_NormalisedCurr =[]
  Global_QtyPerLeg = 1

    # check current positions from IB
  if incomingCUR2=='':
    return 'Y'
  else:
    print('incomingCUR2 =', incomingCUR2)
    optionobj =incomingCUR2.count('(')
    checkLeg = []
    checkPosition = []
    checkPOS = []
    strikes = []
    callput =[]
    legqty = []
    ttlLeg = []
    pos2 = 0
    for i in range(0, optionobj):
        pos1 = incomingCUR2.find('(',pos2)
        pos2 = incomingCUR2.find(')',pos1)
        checkPosition.insert(i, str(incomingCUR2)[pos1+1:pos2])
        #print('-> checkPosition[%d]=%s' %(i,checkPosition[i]))
        checkPOS.append(eval('[' + checkPosition[i] + ']'))

    #print('checkPOS=%s' % (checkPOS))
    Global_NormalisedCurr = checkPOS

    #print('optionobj = %d' % (optionobj))
    for i in range(0, optionobj):


        numlegs = checkPOS[i][2].count('P') + checkPOS[i][2].count('C')
        numslash = checkPOS[i][2].count('/')
        print('1. checkPOS=', checkPOS[i])
        print('1. numlegs=', numlegs)
        print('1. numslash=', numslash)

        if numlegs == 1 and numslash == 1:

            strikes.append(checkPOS[i][2][2:])
            callput.append(checkPOS[i][2][1:2])
            legqty.append(int(checkPOS[i][3])* -1)

        elif numlegs == 1 and numslash == 0:

            strikes.append(checkPOS[i][2][1:])
            callput.append(checkPOS[i][2][:1])
            legqty.append(int(checkPOS[i][3]))

        elif numlegs == 1 and numslash == 1:

            strikes.append(checkPOS[i][2][1:])
            callput.append(checkPOS[i][2][:1])
            legqty.append(int(checkPOS[i][3])* -1)

        elif numlegs == 2 and numslash == 1:

            strikes.append(checkPOS[i][2][1:find_nth(checkPOS[i][2], "/", 1)])
            strikes.append(checkPOS[i][2][find_nth(checkPOS[i][2], "/", 1) + 2:])
            callput.append(checkPOS[i][2][:1])
            callput.append(checkPOS[i][2][find_nth(checkPOS[i][2], "/", 1) + 1:find_nth(checkPOS[i][2], "/", 1) + 2])
            legqty.append(int(checkPOS[i][3]))
            legqty.append(int(checkPOS[i][3]) * -1)

        elif numlegs == 4 and numslash == 3:

            strikes.append(checkPOS[i][2][1:find_nth(checkPOS[i][2], "/", 1)])
            strikes.append(checkPOS[i][2][find_nth(checkPOS[i][2], "/", 1) + 2:find_nth(checkPOS[i][2], "/", 2)])
            strikes.append(checkPOS[i][2][find_nth(checkPOS[i][2], "/", 2) + 2:find_nth(checkPOS[i][2], "/", 3)])
            strikes.append(checkPOS[i][2][find_nth(checkPOS[i][2], "/", 3) + 2:])
            callput.append(checkPOS[i][2][:1])
            callput.append(checkPOS[i][2][find_nth(checkPOS[i][2], "/", 1) + 1:find_nth(checkPOS[i][2], "/", 1) + 2])
            callput.append(checkPOS[i][2][find_nth(checkPOS[i][2], "/", 2) + 1:find_nth(checkPOS[i][2], "/", 2) + 2])
            callput.append(checkPOS[i][2][find_nth(checkPOS[i][2], "/", 3) + 1:find_nth(checkPOS[i][2], "/", 3) + 2])
            legqty.append(int(checkPOS[i][3]))
            legqty.append(int(checkPOS[i][3]) * -1)
            legqty.append(int(checkPOS[i][3]) * -1)
            legqty.append(int(checkPOS[i][3]))

        elif numlegs == 2 and numslash == 3:

            strikes.append(checkPOS[i][2][1:find_nth(checkPOS[i][2], "/", 1)])
            strikes.append(checkPOS[i][2][find_nth(checkPOS[i][2], "/", 3) + 2:])
            callput.append(checkPOS[i][2][:1])
            callput.append(checkPOS[i][2][find_nth(checkPOS[i][2], "/", 3) + 1:find_nth(checkPOS[i][2], "/", 3) + 2])
            legqty.append(int(checkPOS[i][3]))
            legqty.append(int(checkPOS[i][3]))

    #print('->callput=', callput)
    #print('->strikes=', strikes)
    #print('->qty=', legqty)

    for i in range(0, len(callput)):
        checkLeg.extend(eval("[" + checkPosition[0][:find_nth(checkPosition[0], "'", 4) + 1] + "]"))
        checkLeg.append(strikes[i])
        checkLeg.append(callput[i])
        checkLeg.append(legqty[i])
        ttlLeg.append(checkLeg)
        #print('11. checkLeg=%s' % (checkLeg))
        checkLeg= []
        #print('11. ttlLeg[%d]=%s' % (i, ttlLeg[i]))

        optionleg9 = []
        for x in range(0, len(ttlLeg)):
            optionleg9.append(ttlLeg[x])

        optionleg6 = []
        for x in range(0, len(ttlLeg)):
            optionleg6.append(ttlLeg[x])

    print('1. optionleg6=',optionleg6)
    optionleg7 = []

    optionleg7 = Removedup101(optionleg6)
    #print('2. optionleg7=',optionleg7)

    #print('len(optionleg7=',len(optionleg7))
    for x in range(0,len(optionleg7)):
        #print('2. optionleg7[%d]=%s' % (x,optionleg7[x][4]))
        optionleg7[x][4]=optionleg7[x][4] * Global_QtyPerLeg

    #print('3. optionleg7=', optionleg7)
    Global_Optionleg = optionleg7
    #print('4. Global_Optionleg=', Global_Optionleg)

    optionVar = []
    optionIB = []
    returnVal = "N"
    ib = IB()
    ib.connect(TWS_IP_Address, 7496, clientId=170)
    currentPositions=ib.positions()
    print('1. ib=',ib)
    ib.disconnect()
    totalNumberPositions = len(currentPositions)
    #print('totalNumberPositions =', totalNumberPositions)

    for j in range(0, optionobj):

        #print("current checking position=",incomingCUR2)
        #incomingCUR3 = eval('[' + incomingCUR2 + ']')

        #print('incomingCUR3=', incomingCUR3)
        for x in range(0, totalNumberPositions):
            #print("-> currentPositions[%d] = %s" % (x, currentPositions[x]))

            pos1 = str(currentPositions[x]).find("symbol='")
            pos2 = str(currentPositions[x]).find("'", pos1+8)
            optionVar.insert(0,str(currentPositions[x])[pos1+8:pos2])
            pos1 = str(currentPositions[x]).find("lastTradeDateOrContractMonth='")
            pos2 = str(currentPositions[x]).find("'", pos1+30)
            optionVar.insert(1, str(currentPositions[x])[pos1+30:pos2])
            pos1 = str(currentPositions[x]).find("strike=")
            pos2 = str(currentPositions[x]).find(".", pos1+7)
            optionVar.insert(2, str(currentPositions[x])[pos1+7:pos2])
            pos1 = str(currentPositions[x]).find("right='")
            pos2 = str(currentPositions[x]).find("'", pos1+7)
            optionVar.insert(3, str(currentPositions[x])[pos1+7:pos2])
            pos1 = str(currentPositions[x]).find("position=")
            pos2 = str(currentPositions[x]).find(".", pos1+9)
            optionVar.insert(4, str(currentPositions[x])[pos1+9:pos2])

            optionIB.insert(x, [optionVar[0], optionVar[1], optionVar[2], optionVar[3], int(optionVar[4])])

    icountmatch =0

    #print('optionIB=',optionIB)
    for i in range(0, len(optionleg7)):
        for j in range(0, len(currentPositions)):
            checkmatch1 = set(optionleg7[i]) & set(optionIB[j])
            if len(checkmatch1)==5 or (len(checkmatch1)==4 and abs(optionIB[j][4])>abs(optionleg7[i][4])):
                icountmatch = icountmatch + 1
                #print('1. icountmatch=%d optionleg7[%d]=%s optionIB[%d]=%s' % (icountmatch, i, optionleg7[i], j, optionIB[j]))
                #print('2. optionleg7[%d][4]=%s optionIB[%d][4]=%s' % (i, optionleg7[i][4], j, optionIB[j][4]))

    #print('-> optionleg7=', optionleg7)
    #print('icountmatch=',icountmatch)
    if icountmatch==len(optionleg7):
        print('Current Positions Match Expected Positions..')
        returnVal = "Y"
    else:
        print('Current Positions DO NOT Match Expected Positions..')
        returnVal = "N"
    return returnVal