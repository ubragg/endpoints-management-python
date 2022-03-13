# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Generated client library for servicecontrol version v1."""
from __future__ import absolute_import
# NOTE: This file is autogenerated and should not be edited by hand.
from apitools.base.py import base_api
from . import servicecontrol_v1_messages as messages


class ServicecontrolV1(base_api.BaseApiClient):
  """Generated client library for service servicecontrol version v1."""

  MESSAGES_MODULE = messages
  BASE_URL = u'https://servicecontrol.googleapis.com/'

  _PACKAGE = u'servicecontrol'
  _SCOPES = [u'https://www.googleapis.com/auth/cloud-platform', u'https://www.googleapis.com/auth/servicecontrol']
  _VERSION = u'v1'
  _CLIENT_ID = '1042881264118.apps.googleusercontent.com'
  _CLIENT_SECRET = 'x_Tw5K8nnjoRAqULM9PFAC2b'
  _USER_AGENT = 'x_Tw5K8nnjoRAqULM9PFAC2b'
  _CLIENT_CLASS_NAME = u'ServicecontrolV1'
  _URL_VERSION = u'v1'
  _API_KEY = None

  def __init__(self, url='', credentials=None,
               get_credentials=True, http=None, model=None,
               log_request=False, log_response=False,
               credentials_args=None, default_global_params=None,
               additional_http_headers=None):
    """Create a new servicecontrol handle."""
    url = url or self.BASE_URL
    super(ServicecontrolV1, self).__init__(
        url, credentials=credentials,
        get_credentials=get_credentials, http=http, model=model,
        log_request=log_request, log_response=log_response,
        credentials_args=credentials_args,
        default_global_params=default_global_params,
        additional_http_headers=additional_http_headers)
    self.services = self.ServicesService(self)

  class ServicesService(base_api.BaseApiService):
    """Service class for the services resource."""

    _NAME = u'services'

    def __init__(self, client):
      super(ServicecontrolV1.ServicesService, self).__init__(client)
      self._upload_configs = {
          }

    def AllocateQuota(self, request, global_params=None):
      """Attempts to allocate quota for the specified consumer. It should be called.
before the operation is executed.

This method requires the `servicemanagement.services.quota`
permission on the specified service. For more information, see
[Google Cloud IAM](https://cloud.google.com/iam).

**NOTE:** the client code **must** fail-open if the server returns one
of the following quota errors:
-   `PROJECT_STATUS_UNAVAILABLE`
-   `SERVICE_STATUS_UNAVAILABLE`
-   `BILLING_STATUS_UNAVAILABLE`
-   `QUOTA_SYSTEM_UNAVAILABLE`

The server may inject above errors to prohibit any hard dependency
on the quota system.

      Args:
        request: (ServicecontrolServicesAllocateQuotaRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (AllocateQuotaResponse) The response message.
      """
      config = self.GetMethodConfig('AllocateQuota')
      return self._RunMethod(
          config, request, global_params=global_params)

    AllocateQuota.method_config = lambda: base_api.ApiMethodInfo(
        http_method=u'POST',
        method_id=u'servicecontrol.services.allocateQuota',
        ordered_params=[u'serviceName'],
        path_params=[u'serviceName'],
        query_params=[],
        relative_path=u'v1/services/{serviceName}:allocateQuota',
        request_field=u'allocateQuotaRequest',
        request_type_name=u'ServicecontrolServicesAllocateQuotaRequest',
        response_type_name=u'AllocateQuotaResponse',
        supports_download=False,
    )

    def Check(self, request, global_params=None):
      """Checks an operation with Google Service Control to decide whether.
the given operation should proceed. It should be called before the
operation is executed.

If feasible, the client should cache the check results and reuse them for
60 seconds. In case of server errors, the client can rely on the cached
results for longer time.

NOTE: the CheckRequest has the size limit of 64KB.

This method requires the `servicemanagement.services.check` permission
on the specified service. For more information, see
[Google Cloud IAM](https://cloud.google.com/iam).

      Args:
        request: (ServicecontrolServicesCheckRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (CheckResponse) The response message.
      """
      config = self.GetMethodConfig('Check')
      return self._RunMethod(
          config, request, global_params=global_params)

    Check.method_config = lambda: base_api.ApiMethodInfo(
        http_method=u'POST',
        method_id=u'servicecontrol.services.check',
        ordered_params=[u'serviceName'],
        path_params=[u'serviceName'],
        query_params=[],
        relative_path=u'v1/services/{serviceName}:check',
        request_field=u'checkRequest',
        request_type_name=u'ServicecontrolServicesCheckRequest',
        response_type_name=u'CheckResponse',
        supports_download=False,
    )

    def EndReconciliation(self, request, global_params=None):
      """Signals the quota controller that service ends the ongoing usage.
reconciliation.

This method requires the `servicemanagement.services.quota`
permission on the specified service. For more information, see
[Google Cloud IAM](https://cloud.google.com/iam).

      Args:
        request: (ServicecontrolServicesEndReconciliationRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (EndReconciliationResponse) The response message.
      """
      config = self.GetMethodConfig('EndReconciliation')
      return self._RunMethod(
          config, request, global_params=global_params)

    EndReconciliation.method_config = lambda: base_api.ApiMethodInfo(
        http_method=u'POST',
        method_id=u'servicecontrol.services.endReconciliation',
        ordered_params=[u'serviceName'],
        path_params=[u'serviceName'],
        query_params=[],
        relative_path=u'v1/services/{serviceName}:endReconciliation',
        request_field=u'endReconciliationRequest',
        request_type_name=u'ServicecontrolServicesEndReconciliationRequest',
        response_type_name=u'EndReconciliationResponse',
        supports_download=False,
    )

    def ReleaseQuota(self, request, global_params=None):
      """Releases previously allocated quota done through AllocateQuota method.

This method requires the `servicemanagement.services.quota`
permission on the specified service. For more information, see
[Google Cloud IAM](https://cloud.google.com/iam).

**NOTE:** the client code **must** fail-open if the server returns one
of the following quota errors:
-   `PROJECT_STATUS_UNAVAILABLE`
-   `SERVICE_STATUS_UNAVAILABLE`
-   `BILLING_STATUS_UNAVAILABLE`
-   `QUOTA_SYSTEM_UNAVAILABLE`

The server may inject above errors to prohibit any hard dependency
on the quota system.

      Args:
        request: (ServicecontrolServicesReleaseQuotaRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ReleaseQuotaResponse) The response message.
      """
      config = self.GetMethodConfig('ReleaseQuota')
      return self._RunMethod(
          config, request, global_params=global_params)

    ReleaseQuota.method_config = lambda: base_api.ApiMethodInfo(
        http_method=u'POST',
        method_id=u'servicecontrol.services.releaseQuota',
        ordered_params=[u'serviceName'],
        path_params=[u'serviceName'],
        query_params=[],
        relative_path=u'v1/services/{serviceName}:releaseQuota',
        request_field=u'releaseQuotaRequest',
        request_type_name=u'ServicecontrolServicesReleaseQuotaRequest',
        response_type_name=u'ReleaseQuotaResponse',
        supports_download=False,
    )

    def Report(self, request, global_params=None):
      """Reports operation results to Google Service Control, such as logs and.
metrics. It should be called after an operation is completed.

If feasible, the client should aggregate reporting data for up to 5
seconds to reduce API traffic. Limiting aggregation to 5 seconds is to
reduce data loss during client crashes. Clients should carefully choose
the aggregation time window to avoid data loss risk more than 0.01%
for business and compliance reasons.

NOTE: the ReportRequest has the size limit of 1MB.

This method requires the `servicemanagement.services.report` permission
on the specified service. For more information, see
[Google Cloud IAM](https://cloud.google.com/iam).

      Args:
        request: (ServicecontrolServicesReportRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ReportResponse) The response message.
      """
      config = self.GetMethodConfig('Report')
      return self._RunMethod(
          config, request, global_params=global_params)

    Report.method_config = lambda: base_api.ApiMethodInfo(
        http_method=u'POST',
        method_id=u'servicecontrol.services.report',
        ordered_params=[u'serviceName'],
        path_params=[u'serviceName'],
        query_params=[],
        relative_path=u'v1/services/{serviceName}:report',
        request_field=u'reportRequest',
        request_type_name=u'ServicecontrolServicesReportRequest',
        response_type_name=u'ReportResponse',
        supports_download=False,
    )

    def StartReconciliation(self, request, global_params=None):
      """Unlike rate quota, allocation quota does not get refilled periodically.
So, it is possible that the quota usage as seen by the service differs from
what the One Platform considers the usage is. This is expected to happen
only rarely, but over time this can accumulate. Services can invoke
StartReconciliation and EndReconciliation to correct this usage drift, as
described below:
1. Service sends StartReconciliation with a timestamp in future for each
   metric that needs to be reconciled. The timestamp being in future allows
   to account for in-flight AllocateQuota and ReleaseQuota requests for the
   same metric.
2. One Platform records this timestamp and starts tracking subsequent
   AllocateQuota and ReleaseQuota requests until EndReconciliation is
   called.
3. At or after the time specified in the StartReconciliation, service
   sends EndReconciliation with the usage that needs to be reconciled to.
4. One Platform adjusts its own record of usage for that metric to the
   value specified in EndReconciliation by taking in to account any
   allocation or release between StartReconciliation and EndReconciliation.

Signals the quota controller that the service wants to perform a usage
reconciliation as specified in the request.

This method requires the `servicemanagement.services.quota`
permission on the specified service. For more information, see
[Google Cloud IAM](https://cloud.google.com/iam).

      Args:
        request: (ServicecontrolServicesStartReconciliationRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (StartReconciliationResponse) The response message.
      """
      config = self.GetMethodConfig('StartReconciliation')
      return self._RunMethod(
          config, request, global_params=global_params)

    StartReconciliation.method_config = lambda: base_api.ApiMethodInfo(
        http_method=u'POST',
        method_id=u'servicecontrol.services.startReconciliation',
        ordered_params=[u'serviceName'],
        path_params=[u'serviceName'],
        query_params=[],
        relative_path=u'v1/services/{serviceName}:startReconciliation',
        request_field=u'startReconciliationRequest',
        request_type_name=u'ServicecontrolServicesStartReconciliationRequest',
        response_type_name=u'StartReconciliationResponse',
        supports_download=False,
    )
