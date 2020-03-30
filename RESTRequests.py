# -*- coding:utf-8 -*-
import json
import requests
requests.packages.urllib3.disable_warnings()
def printResponse(response):
        print("Response code " + str(response.status_code) + ' for url : ' + str(response.url))
        if response.status_code == requests.codes.ok:
                print("Status is : " + str(requests.codes.ok))
        print("Response text : " + prettyString(response.text))
        #print("Response header :" + str(response.headers))
        #print("Response data " + str(response.content))
        #print("Cookies : " + str(response.cookies.get_dict()))

def prettyString(json_string):
        return json.dumps(json.loads(json_string), indent=4)

class REST:
    def doGetRequest(self,route,params=None,headers=None,cookies={},proxies=None,catch_response=True,verify=False):
        # print("GET Request Header = " + str(headers))
        # print("GET Request ="+str(route)+str(params))
        # #self.params = json.dumps(self.params,indent=4)

        with requests.get(route, params=params, headers = headers, cookies=cookies, proxies=proxies,verify=verify) as response:
            # printResponse(response)
            if response.content == "":
                response.failure("No data")
        return response

    def doPost(self,route,params=None,payload={},files={},headers=None,proxies=None):
        #print "Proxies = "+ str(self.proxies)
        #print("POST Request Payload = " + payload)
        print("POST Request Header = " + str(headers))
        print("POST Params = " + str(params))
        with requests.post(route, params=params ,headers=headers, data=payload, files=files, proxies=proxies) as response:
            printResponse(response)
            print("Post done!")
        return response