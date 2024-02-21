#!/bin/bash

#URL="https://192.168.56.70:6443/api/v1/namespaces/default/pods"
URL="https://192.168.56.70:6443/api/v1/pods"
#TOKEN=$(kubectl get secrets api-token -o=jsonpath='{.data.token}' | base64 -d)
TOKEN="eyJhbGciOiJSUzI1NiIsImtpZCI6IlJkU3hFWHZ2ZElDQXRweEp6dE8tZDhHeWZTeFI0RGdOd3FEQjk0VmpWTkEifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwiXSwiZXhwIjoxNzA4MzE2ODI2LCJpYXQiOjE3MDgzMTMyMjYsImlzcyI6Imh0dHBzOi8va3ViZXJuZXRlcy5kZWZhdWx0LnN2Yy5jbHVzdGVyLmxvY2FsIiwia3ViZXJuZXRlcy5pbyI6eyJuYW1lc3BhY2UiOiJkZWZhdWx0Iiwic2VydmljZWFjY291bnQiOnsibmFtZSI6ImRldi11c2VyLXNhIiwidWlkIjoiZjMzMWY0NjgtODFiNC00Y2ExLWJmZTItMjUwZGZjMDIzYTc5In19LCJuYmYiOjE3MDgzMTMyMjYsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRldi11c2VyLXNhIn0.nIfGf5PWzzxRa0JdwU3grAmUX_MCWVO2xFMXQJo5jqzgT95GoG_A-kyfX00m2BOy3dgbpIbcP-zRnPh2UtTSXQn7evzr486fEwGk12eajpxDQ64MeViHnlm91cBFZUNx3jjn0DXAjFd07lFPEIBjm8SAyp-X170AO-E66G0AHdTVaKnoenNQpUrewl6eoyeNBS-uj4N8gp1BMHoqco1CevE5dh-osHymKaxMk2SwK82trA1kT2kCBPPKbbTue4s0zXJ73EoolfvqFQV6Ww1LuMAU9CUuV2YB8jl6TT12HelJV6ChBpGh84jnPmWzl98-h5EXYhemberWuuaReVhtxQ"

echo $TOKEN
#TOKEN=$(kubectl get secrets -o jsonpath="{.items[?(@.metadata.annotations['kubernetes\.io/service-account\.name']=='default')].data.token}")
get_token() 
{
   curl_output=$(curl -sk -H "Authorization: Bearer $TOKEN" $URL)
   echo "$curl_output"




}

get_token
