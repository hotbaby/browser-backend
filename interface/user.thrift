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

namespace py usr

const string VERSION = "0.1.0"

#
# data structures
#

#
# Exceptions
# (note that internal server errors will raise a TApplicationException, courtesy of Thrift)
#


#
# service api
#
/** 
 * User service comments.
 */
service User extends shared.Base {

  /**
   * Create user
   * @param username.
   * @param passwd.
   * @return.
   */
  bool create(1: required string username, 2: required string passwd)
       throws (1:shared.InvalidRequestException ire),

  /**
   * Update user
   * @param username.
   * @param passwd.
   * @return.
   */
  bool update(1: required string username, 2: required string passwd)
       throws (1:shared.InvalidRequestException ire),

  /**
   * Remove User. "delete" is reversed keyword in thrift, hence, replaced with "remove"
   * @param username.
   * @return.
   */
  bool remove(1: required string username) throws (1:shared.InvalidRequestException ire),

  /**
   * Whether the user is existed or not.
   * @param username.
   * @return.
   */ 
  bool exist(1: required string username) throws (1:shared.InvalidRequestException ire),
}
