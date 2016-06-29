#!/usr/local/bin/thrift --java --php --py
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file # distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# *** PLEASE REMEMBER TO EDIT THE VERSION CONSTANT WHEN MAKING CHANGES ***
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#
# Interface defsnition for Heardbeat Service
#

/**
 * The first thing to know about are types. The available types in Thrift are:
 *
 *  bool        Boolean, one byte
 *  byte        Signed byte
 *  i16         Signed 16-bit integer
 *  i32         Signed 32-bit integer
 *  i64         Signed 64-bit integer
 *  double      64-bit floating point value
 *  string      String
 *  binary      Blob (byte array)
 *  map<t1,t2>  Map from one type to another
 *  list<t1>    Ordered list of one type
 *  set<t1>     Set of unique elements of one type
 *
 * Did you also notice that Thrift supports C style comments?
 */

include "shared.thrift"

namespace py srvtracker

const string VERSION = "0.1.0"

#
# data structures
#



/**
 * Service Registry information.
 */
struct ServiceRegistryInfo {
  1: required string name,
  2: required string host,
}

/**
 * Service Registry Respnse info.
 */
struct ServiceRegistryResponse {
  1: required i32 result,
  2: required i32 id,
  3: required i16 port, 
}

/**
 * Service Profile
 */
struct ServiceProfile {
  1: required i32 id,
  2: required string name,
  3: required string host,
  4: required i16 port,
}

/**
 * HeartbeatMessage
 */
struct HeartbeatMessage {
  1: required i32 service_id,
}

/**
 * HeartbeatResponse
 */
struct HeartbeatResponse {
  1: required i32 result,
}

#
# Exceptions
# (note that internal server errors will raise a TApplicationException, courtesy of Thrift)
#


#
# service api
#
/** 
 * Service Tracker comments
 */
service ServiceTracker extends shared.Base {

  /**
   * Register service
   * @param info. The information of service to register.
   * @return. Return service id. -1 if register error, others >= 0
   */
  ServiceRegistryResponse register_service(1: required ServiceRegistryInfo info) throws (1:shared.InvalidRequestException ire),

  /**
   * Heartbeat message
   * @param msg. The message of heartbeat.
   * @return response. 
   * 
   */
  HeartbeatResponse heartbeat(1: required HeartbeatMessage msg) throws (1:shared.InvalidRequestException ire),

  /**
   * Get service profile.
   * @param name. The service name.
   * @return. Return ServiceProfile if the service exist. Otherwise, ServiceProfile.id is -1 and all the ServiceProfile attributes is invalid.
   */
  ServiceProfile get_service(1: required string name) throws (1:shared.InvalidRequestException ire), 

  /**
   * Get all services info
   * @return. Return the list of all service profile.
   */
  list<ServiceProfile> get_services() throws (1: shared.InvalidRequestException ire),
}
