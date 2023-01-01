import bs4, xmltodict, json
from bs4 import BeautifulSoup 
import requests

def crwl_bus(key):
    serviceKey='5ymRA7zWPfclDo4zJfdQ3N2eMFOemjQJGFRi%2FH8aQegMiaGWRF2qVtLOy4yp6HL6wtWB%2BNVES1DHGze0EbliAQ%3D%3D'
    url="http://apis.data.go.kr/6260000/BusanBIMS/stopArrByBstopid?bstopid=208960201& &serviceKey={}".format(serviceKey)
    #get으로 요청함
    response=requests.get(url).content
    #xml파일을 dict로 파싱하여 사용
    dict=xmltodict.parse(response)
    #원하는 데이터가 ServiceResult 내부 msgBody 내부 itemList내부에 있음 
    #다시 dict로 받은 값을 Json로 변환 
    jsonString=json.dumps(dict['response']['body']['items']['item'],ensure_ascii=False)
    # #json을 형태로 받은 데이터를 Python의 객체로 변환 (dict)
    jsonObj=json.loads(jsonString)

    bus_number_data = {}
    first_time_data = {}
    second_time_data = {}

    #json 파일 형식을 저장
    for i in range(len(jsonObj)):
        bus_number_data[i]='{}'.format(jsonObj[i]['lineno'])
        first_time_data[i]='{}'.format(jsonObj[i]['min1'])
        second_time_data[i]='{}'.format(jsonObj[i]['min2'])

    busNo_128 = bus_number_data[0]
    busNo_129 = bus_number_data[1]
    busNo_62 = bus_number_data[2]

    first_128 = first_time_data[0]
    first_129 = first_time_data[1]
    first_62 = first_time_data[2]

    second_128 = second_time_data[0]
    second_129 = second_time_data[1]
    second_62 = second_time_data[2]

    # 크롤링 확인용 코드
    """
    print("[busss]") 
    print(busNo_128, busNo_129, busNo_62, 
        first_128, first_129, first_62, 
        second_128, second_129, second_62,)
    """

    if key == 0:
        #배열로 넘겨줌
        buses = []

        try:
            buses.append(busNo_128)
            buses.append(first_128)
            buses.append(second_128)
            buses.append(busNo_129)
            buses.append(first_129)
            buses.append(second_129)
            buses.append(busNo_62)
            buses.append(first_62)
            buses.append(second_62)
        except IndexError:
            pass
        return buses
    elif key == 1:
        buses=''
        for i in range(len(jsonObj)):
            buses+='{}\n 첫번째도착시간: {}분 \n 두번째도착시간: {}분 \n'.format(jsonObj[i]['lineno'],jsonObj[i]['min1'],jsonObj[i]['min2'])     
        return buses


if __name__ == "__main__":
    crwl_bus() 