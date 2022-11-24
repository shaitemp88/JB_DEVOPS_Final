"""Module providingFunction printing python version."""
from __future__ import print_function
import os
import time
import boto3
#import pythonjsonlogger
#from pythonjsonlogger import jsonlogger

# Project configuration settings - Environment variables
ACCESS_ID = os.environ['aws_access_key_id']
ACCESS_KEY = os.environ['aws_secret_access_key']
REGION = os.environ['region']
INTERVAL = int(os.environ["INTERVAL"])

print ("=                   =")
print ("Envoronment Variable:")
print (ACCESS_ID)
print (ACCESS_KEY)
print (REGION)
print (INTERVAL)
print ("=====================")

while True:
    try:
      ec2 = boto3.resource('ec2', region_name=REGION, aws_access_key_id=ACCESS_ID,
                           aws_secret_access_key=ACCESS_KEY)
      instances = ec2.instances.filter(
          Filters=[
              {
                  'Name': 'tag:Name',
                  'Values': [
                      "instance-state-code",
                      "tag:k8s.io/role/master"
                  ]
              },
              {
                  'Name': 'instance-state-code',
                  'Values': [
                      "16"
                  ]
              }
          ]
      )
      for instance in instances:
          for tag in instance.tags:
              print (tag)
          print ("instance id: ", instance.id)
    exception:
      print ("=Exception=")
    print ("Done - waiting for next interval")
    time.sleep(INTERVAL)
