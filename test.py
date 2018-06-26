from time import time

# Requires requests library. Install using pip
import requests


class EapiRequests(object):
    """Allows to make requests to EAPI on given setup."""

    def __init__(self, eapi_url, rui_url, user_name, user_password):
        """
        :param eapi_url: Eapi address on tested setup in following format: ^http[s]?:\/\/[a-z0-9\.-]+\.com$
        :type eapi_url: str
        :param rui_url: Rui address on tested setup in following format: ^http[s]?:\/\/[a-z0-9\.-]+\.com$
        :type rui_url: str
        :type user_name: str
        :type user_password: str
        """
        self.eapi_url = eapi_url + '/rest/'
        self.rui_url = rui_url + '/oauth/token'
        self.user_name = user_name
        self.user_password = user_password
        self.token = self._generate_token()

    def request(self, method, command, **kwargs):
        """Creates request to EAPI.
        See http://docs.python-requests.org/en/master/api/ for documentation on arguments.
        """
        response = requests.request(method.upper(), self.eapi_url + command, headers={
            'Authorization': self.token, 'Content-Type': 'application/json'}, verify=False,
                                    **kwargs)
        return response

    def _generate_token(self):
        """Returns token used for authentication"""
        return 'bearer ' + requests.post(url=self.rui_url,
                                         data={'grant_type': 'password',
                                               'password': self.user_password,
                                               'response_type': 'token',
                                               'username': self.user_name},
                                         verify=False
                                         ).json()['access_token']

    def test_get_all_alerts_on_agent(self):
        response=eapi_requests.request('GET', '2.0/devices/alarms')
        if response.status_code != 200:
            print('Jest bug!')
        else:
            print('ok')
        return response.json()

# Example usage:


# Create EapiRequests object using given setup/user parameters
eapi_requests = EapiRequests(eapi_url='https://eapigeic-qa2.proximetry.com',
                             rui_url='https://geic-qa2.proximetry.com',
                             user_name='user04',
                             user_password='P@ssw0rd')
# Send request to retrieve details about first device from systems
systems_response = eapi_requests.request('GET', '2.0/systems', params={'limit': 1})
# Retrieve asdid from response
asdid = systems_response.json()[0]['asdid']
# Set alarm for device identified by asdid taken from system
set_alarm_response = eapi_requests.request('PATCH',
                                           '2.0/devices/{}/alarms'.format(asdid),
                                           json={
                                               "data": [
                                                   {
                                                       "alarm_id": "test_alarm_1",
                                                       "action": "SET",
                                                       "timestamp": int(time()) * 1000,
                                                       "severity": "EMERGENCY",
                                                       "description": "Device overheating",
                                                       "details": "Temperature is above safe levels",
                                                       "optional": {}
                                                   }
                                               ]
                                           }
                                           )

activation_codes = eapi_requests.request('GET', '2.0/activation_codes')
print(activation_codes.json())



def test_get_alarm(method, endpoint):
    response=eapi_requests.request(method, endpoint)
    if response.status_code != 200:
        raise ValueError('Mamy buga')
    return response.json()


def test_patch_alarms(asdid, severity, idtest):
    response=eapi_requests.request('PATCH',
                          '2.0/devices/{}/alarms'.format(asdid),
                          json={
                              "data": [
                                  {
                                      "alarm_id": str(idtest),
                                      "action": "SET",
                                      "timestamp": int(time()) * 1000,
                                      "severity": str(severity),
                                      "description": "Device overheating",
                                      "details": "Temperature is above safe levels",
                                      "optional": {}
                                  }
                              ]
                          }
                          )
    if response.status_code !=200:
        raise ValueError('There is no new alarm created')
    else:
        return response.json()

def test_change_alarm_action(asdid, idtest, action):
    response = eapi_requests.request('PATCH',
                                     '2.0/devices/{}/alarms'.format(asdid),
                                     json={
                                         "data": [
                                             {
                                                 "alarm_id": str(idtest),
                                                 "action": str(action),
                                                 "timestamp": int(time()) * 1000,
                                                 "severity": 'MAJOR',
                                                 "description": "Device overheating",
                                                 "details": "Temperature is above safe levels",
                                                 "optional": {}
                                             }
                                         ]
                                     }
                                     )
    if response.status_code != 200:
        raise ValueError('You didn\'t change action in these alarm')
    else:
        return response.json()

def test_change_alarm_severity():
    pass

def test_delete_alarm_by_id(method,endpoint, idalarm):
    pass

def test_delete_all_alarms():
    pass

def get_alarm_with_specified_id():
    pass

#print(test_get_alarm('GET', '2.0/devices/3EEBD96DC634/alarms'))
#print(test_patch_alarms('3EEBD96DC634', 'MAJOR', 'Alarm3'))
#print(test_change_alarm_action('3EEBD96DC634', 'Alarm3', 'CLEAR'))

