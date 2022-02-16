# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from collections import OrderedDict
import functools
import re
from typing import Dict, Optional, Sequence, Tuple, Type, Union
import pkg_resources

from google.api_core.client_options import ClientOptions
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.certificate_manager_v1.services.certificate_manager import pagers
from google.cloud.certificate_manager_v1.types import certificate_manager
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import CertificateManagerTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import CertificateManagerGrpcAsyncIOTransport
from .client import CertificateManagerClient


class CertificateManagerAsyncClient:
    """API Overview

    Certificates Manager API allows customers to see and manage all
    their TLS certificates.

    Certificates Manager API service provides methods to manage
    certificates, group them into collections, and create serving
    configuration that can be easily applied to other Cloud resources
    e.g. Target Proxies.

    Data Model

    The Certificates Manager service exposes the following resources:

    -  ``Certificate`` which describes a single TLS certificate.
    -  ``CertificateMap`` which describes a collection of certificates
       that can be attached to a target resource.
    -  ``CertificateMapEntry`` which describes a single configuration
       entry that consists of a SNI and a group of certificates. It's a
       subresource of CertificateMap.

    Certificate, CertificateMap and CertificateMapEntry IDs have to
    match "^[a-z0-9-]{1,63}$" regexp, which means that

    -  only lower case letters, digits, and hyphen are allowed
    -  length of the resource ID has to be in [1,63] range.

    Provides methods to manage Cloud Certificate Manager entities.
    """

    _client: CertificateManagerClient

    DEFAULT_ENDPOINT = CertificateManagerClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = CertificateManagerClient.DEFAULT_MTLS_ENDPOINT

    certificate_path = staticmethod(CertificateManagerClient.certificate_path)
    parse_certificate_path = staticmethod(
        CertificateManagerClient.parse_certificate_path
    )
    certificate_map_path = staticmethod(CertificateManagerClient.certificate_map_path)
    parse_certificate_map_path = staticmethod(
        CertificateManagerClient.parse_certificate_map_path
    )
    certificate_map_entry_path = staticmethod(
        CertificateManagerClient.certificate_map_entry_path
    )
    parse_certificate_map_entry_path = staticmethod(
        CertificateManagerClient.parse_certificate_map_entry_path
    )
    dns_authorization_path = staticmethod(
        CertificateManagerClient.dns_authorization_path
    )
    parse_dns_authorization_path = staticmethod(
        CertificateManagerClient.parse_dns_authorization_path
    )
    target_https_proxies_path = staticmethod(
        CertificateManagerClient.target_https_proxies_path
    )
    parse_target_https_proxies_path = staticmethod(
        CertificateManagerClient.parse_target_https_proxies_path
    )
    target_ssl_proxies_path = staticmethod(
        CertificateManagerClient.target_ssl_proxies_path
    )
    parse_target_ssl_proxies_path = staticmethod(
        CertificateManagerClient.parse_target_ssl_proxies_path
    )
    common_billing_account_path = staticmethod(
        CertificateManagerClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        CertificateManagerClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(CertificateManagerClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        CertificateManagerClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        CertificateManagerClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        CertificateManagerClient.parse_common_organization_path
    )
    common_project_path = staticmethod(CertificateManagerClient.common_project_path)
    parse_common_project_path = staticmethod(
        CertificateManagerClient.parse_common_project_path
    )
    common_location_path = staticmethod(CertificateManagerClient.common_location_path)
    parse_common_location_path = staticmethod(
        CertificateManagerClient.parse_common_location_path
    )

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            CertificateManagerAsyncClient: The constructed client.
        """
        return CertificateManagerClient.from_service_account_info.__func__(CertificateManagerAsyncClient, info, *args, **kwargs)  # type: ignore

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            CertificateManagerAsyncClient: The constructed client.
        """
        return CertificateManagerClient.from_service_account_file.__func__(CertificateManagerAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @classmethod
    def get_mtls_endpoint_and_cert_source(
        cls, client_options: Optional[ClientOptions] = None
    ):
        """Return the API endpoint and client cert source for mutual TLS.

        The client cert source is determined in the following order:
        (1) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is not "true", the
        client cert source is None.
        (2) if `client_options.client_cert_source` is provided, use the provided one; if the
        default client cert source exists, use the default one; otherwise the client cert
        source is None.

        The API endpoint is determined in the following order:
        (1) if `client_options.api_endpoint` if provided, use the provided one.
        (2) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is "always", use the
        default mTLS endpoint; if the environment variabel is "never", use the default API
        endpoint; otherwise if client cert source exists, use the default mTLS endpoint, otherwise
        use the default API endpoint.

        More details can be found at https://google.aip.dev/auth/4114.

        Args:
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. Only the `api_endpoint` and `client_cert_source` properties may be used
                in this method.

        Returns:
            Tuple[str, Callable[[], Tuple[bytes, bytes]]]: returns the API endpoint and the
                client cert source to use.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If any errors happen.
        """
        return CertificateManagerClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> CertificateManagerTransport:
        """Returns the transport used by the client instance.

        Returns:
            CertificateManagerTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(CertificateManagerClient).get_transport_class,
        type(CertificateManagerClient),
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, CertificateManagerTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the certificate manager client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.CertificateManagerTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client. It
                won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS_ENDPOINT
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto switch to the
                default mTLS endpoint if client certificate is present, this is
                the default value). However, the ``api_endpoint`` property takes
                precedence if provided.
                (2) If GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide client certificate for mutual TLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        self._client = CertificateManagerClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_certificates(
        self,
        request: Union[certificate_manager.ListCertificatesRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListCertificatesAsyncPager:
        r"""Lists Certificates in a given project and location.

        .. code-block:: python

            from google.cloud import certificate_manager_v1

            def sample_list_certificates():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                request = certificate_manager_v1.ListCertificatesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_certificates(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.ListCertificatesRequest, dict]):
                The request object. Request for the `ListCertificates`
                method.
            parent (:class:`str`):
                Required. The project and location from which the
                certificate should be listed, specified in the format
                ``projects/*/locations/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.certificate_manager_v1.services.certificate_manager.pagers.ListCertificatesAsyncPager:
                Response for the ListCertificates method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = certificate_manager.ListCertificatesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_certificates,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListCertificatesAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_certificate(
        self,
        request: Union[certificate_manager.GetCertificateRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> certificate_manager.Certificate:
        r"""Gets details of a single Certificate.

        .. code-block:: python

            from google.cloud import certificate_manager_v1

            def sample_get_certificate():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                request = certificate_manager_v1.GetCertificateRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_certificate(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.GetCertificateRequest, dict]):
                The request object. Request for the `GetCertificate`
                method.
            name (:class:`str`):
                Required. A name of the certificate to describe. Must be
                in the format ``projects/*/locations/*/certificates/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.certificate_manager_v1.types.Certificate:
                Defines TLS certificate.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = certificate_manager.GetCertificateRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_certificate,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def create_certificate(
        self,
        request: Union[certificate_manager.CreateCertificateRequest, dict] = None,
        *,
        parent: str = None,
        certificate: certificate_manager.Certificate = None,
        certificate_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a new Certificate in a given project and
        location.


        .. code-block:: python

            from google.cloud import certificate_manager_v1

            def sample_create_certificate():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                request = certificate_manager_v1.CreateCertificateRequest(
                    parent="parent_value",
                    certificate_id="certificate_id_value",
                )

                # Make the request
                operation = client.create_certificate(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.CreateCertificateRequest, dict]):
                The request object. Request for the `CreateCertificate`
                method.
            parent (:class:`str`):
                Required. The parent resource of the certificate. Must
                be in the format ``projects/*/locations/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            certificate (:class:`google.cloud.certificate_manager_v1.types.Certificate`):
                Required. A definition of the
                certificate to create.

                This corresponds to the ``certificate`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            certificate_id (:class:`str`):
                Required. A user-provided name of the
                certificate.

                This corresponds to the ``certificate_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.certificate_manager_v1.types.Certificate`
                Defines TLS certificate.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, certificate, certificate_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = certificate_manager.CreateCertificateRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if certificate is not None:
            request.certificate = certificate
        if certificate_id is not None:
            request.certificate_id = certificate_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_certificate,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            certificate_manager.Certificate,
            metadata_type=certificate_manager.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def update_certificate(
        self,
        request: Union[certificate_manager.UpdateCertificateRequest, dict] = None,
        *,
        certificate: certificate_manager.Certificate = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Updates a Certificate.

        .. code-block:: python

            from google.cloud import certificate_manager_v1

            def sample_update_certificate():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                request = certificate_manager_v1.UpdateCertificateRequest(
                )

                # Make the request
                operation = client.update_certificate(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.UpdateCertificateRequest, dict]):
                The request object. Request for the `UpdateCertificate`
                method.
            certificate (:class:`google.cloud.certificate_manager_v1.types.Certificate`):
                Required. A definition of the
                certificate to update.

                This corresponds to the ``certificate`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. The update mask applies to the resource. For
                the ``FieldMask`` definition, see
                https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#fieldmask.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.certificate_manager_v1.types.Certificate`
                Defines TLS certificate.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([certificate, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = certificate_manager.UpdateCertificateRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if certificate is not None:
            request.certificate = certificate
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_certificate,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("certificate.name", request.certificate.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            certificate_manager.Certificate,
            metadata_type=certificate_manager.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def delete_certificate(
        self,
        request: Union[certificate_manager.DeleteCertificateRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deletes a single Certificate.

        .. code-block:: python

            from google.cloud import certificate_manager_v1

            def sample_delete_certificate():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                request = certificate_manager_v1.DeleteCertificateRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_certificate(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.DeleteCertificateRequest, dict]):
                The request object. Request for the `DeleteCertificate`
                method.
            name (:class:`str`):
                Required. A name of the certificate to delete. Must be
                in the format ``projects/*/locations/*/certificates/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

                   The JSON representation for Empty is empty JSON
                   object {}.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = certificate_manager.DeleteCertificateRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_certificate,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=certificate_manager.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def list_certificate_maps(
        self,
        request: Union[certificate_manager.ListCertificateMapsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListCertificateMapsAsyncPager:
        r"""Lists CertificateMaps in a given project and
        location.


        .. code-block:: python

            from google.cloud import certificate_manager_v1

            def sample_list_certificate_maps():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                request = certificate_manager_v1.ListCertificateMapsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_certificate_maps(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.ListCertificateMapsRequest, dict]):
                The request object. Request for the
                `ListCertificateMaps` method.
            parent (:class:`str`):
                Required. The project and location from which the
                certificate maps should be listed, specified in the
                format ``projects/*/locations/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.certificate_manager_v1.services.certificate_manager.pagers.ListCertificateMapsAsyncPager:
                Response for the ListCertificateMaps method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = certificate_manager.ListCertificateMapsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_certificate_maps,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListCertificateMapsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_certificate_map(
        self,
        request: Union[certificate_manager.GetCertificateMapRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> certificate_manager.CertificateMap:
        r"""Gets details of a single CertificateMap.

        .. code-block:: python

            from google.cloud import certificate_manager_v1

            def sample_get_certificate_map():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                request = certificate_manager_v1.GetCertificateMapRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_certificate_map(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.GetCertificateMapRequest, dict]):
                The request object. Request for the `GetCertificateMap`
                method.
            name (:class:`str`):
                Required. A name of the certificate map to describe.
                Must be in the format
                ``projects/*/locations/*/certificateMaps/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.certificate_manager_v1.types.CertificateMap:
                Defines a collection of certificate
                configurations.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = certificate_manager.GetCertificateMapRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_certificate_map,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def create_certificate_map(
        self,
        request: Union[certificate_manager.CreateCertificateMapRequest, dict] = None,
        *,
        parent: str = None,
        certificate_map: certificate_manager.CertificateMap = None,
        certificate_map_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a new CertificateMap in a given project and
        location.


        .. code-block:: python

            from google.cloud import certificate_manager_v1

            def sample_create_certificate_map():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                request = certificate_manager_v1.CreateCertificateMapRequest(
                    parent="parent_value",
                    certificate_map_id="certificate_map_id_value",
                )

                # Make the request
                operation = client.create_certificate_map(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.CreateCertificateMapRequest, dict]):
                The request object. Request for the
                `CreateCertificateMap` method.
            parent (:class:`str`):
                Required. The parent resource of the certificate map.
                Must be in the format ``projects/*/locations/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            certificate_map (:class:`google.cloud.certificate_manager_v1.types.CertificateMap`):
                Required. A definition of the
                certificate map to create.

                This corresponds to the ``certificate_map`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            certificate_map_id (:class:`str`):
                Required. A user-provided name of the
                certificate map.

                This corresponds to the ``certificate_map_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.certificate_manager_v1.types.CertificateMap`
                Defines a collection of certificate configurations.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, certificate_map, certificate_map_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = certificate_manager.CreateCertificateMapRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if certificate_map is not None:
            request.certificate_map = certificate_map
        if certificate_map_id is not None:
            request.certificate_map_id = certificate_map_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_certificate_map,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            certificate_manager.CertificateMap,
            metadata_type=certificate_manager.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def update_certificate_map(
        self,
        request: Union[certificate_manager.UpdateCertificateMapRequest, dict] = None,
        *,
        certificate_map: certificate_manager.CertificateMap = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Updates a CertificateMap.

        .. code-block:: python

            from google.cloud import certificate_manager_v1

            def sample_update_certificate_map():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                request = certificate_manager_v1.UpdateCertificateMapRequest(
                )

                # Make the request
                operation = client.update_certificate_map(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.UpdateCertificateMapRequest, dict]):
                The request object. Request for the
                `UpdateCertificateMap` method.
            certificate_map (:class:`google.cloud.certificate_manager_v1.types.CertificateMap`):
                Required. A definition of the
                certificate map to update.

                This corresponds to the ``certificate_map`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. The update mask applies to the resource. For
                the ``FieldMask`` definition, see
                https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#fieldmask.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.certificate_manager_v1.types.CertificateMap`
                Defines a collection of certificate configurations.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([certificate_map, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = certificate_manager.UpdateCertificateMapRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if certificate_map is not None:
            request.certificate_map = certificate_map
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_certificate_map,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("certificate_map.name", request.certificate_map.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            certificate_manager.CertificateMap,
            metadata_type=certificate_manager.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def delete_certificate_map(
        self,
        request: Union[certificate_manager.DeleteCertificateMapRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deletes a single CertificateMap. A Certificate Map
        can't be deleted if it contains Certificate Map Entries.
        Remove all the entries from the map before calling this
        method.


        .. code-block:: python

            from google.cloud import certificate_manager_v1

            def sample_delete_certificate_map():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                request = certificate_manager_v1.DeleteCertificateMapRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_certificate_map(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.DeleteCertificateMapRequest, dict]):
                The request object. Request for the
                `DeleteCertificateMap` method.
            name (:class:`str`):
                Required. A name of the certificate map to delete. Must
                be in the format
                ``projects/*/locations/*/certificateMaps/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

                   The JSON representation for Empty is empty JSON
                   object {}.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = certificate_manager.DeleteCertificateMapRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_certificate_map,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=certificate_manager.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def list_certificate_map_entries(
        self,
        request: Union[
            certificate_manager.ListCertificateMapEntriesRequest, dict
        ] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListCertificateMapEntriesAsyncPager:
        r"""Lists CertificateMapEntries in a given project and
        location.


        .. code-block:: python

            from google.cloud import certificate_manager_v1

            def sample_list_certificate_map_entries():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                request = certificate_manager_v1.ListCertificateMapEntriesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_certificate_map_entries(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.ListCertificateMapEntriesRequest, dict]):
                The request object. Request for the
                `ListCertificateMapEntries` method.
            parent (:class:`str`):
                Required. The project, location and certificate map from
                which the certificate map entries should be listed,
                specified in the format
                ``projects/*/locations/*/certificateMaps/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.certificate_manager_v1.services.certificate_manager.pagers.ListCertificateMapEntriesAsyncPager:
                Response for the ListCertificateMapEntries method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = certificate_manager.ListCertificateMapEntriesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_certificate_map_entries,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListCertificateMapEntriesAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_certificate_map_entry(
        self,
        request: Union[certificate_manager.GetCertificateMapEntryRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> certificate_manager.CertificateMapEntry:
        r"""Gets details of a single CertificateMapEntry.

        .. code-block:: python

            from google.cloud import certificate_manager_v1

            def sample_get_certificate_map_entry():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                request = certificate_manager_v1.GetCertificateMapEntryRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_certificate_map_entry(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.GetCertificateMapEntryRequest, dict]):
                The request object. Request for the
                `GetCertificateMapEntry` method.
            name (:class:`str`):
                Required. A name of the certificate map entry to
                describe. Must be in the format
                ``projects/*/locations/*/certificateMaps/*/certificateMapEntries/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.certificate_manager_v1.types.CertificateMapEntry:
                Defines a certificate map entry.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = certificate_manager.GetCertificateMapEntryRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_certificate_map_entry,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def create_certificate_map_entry(
        self,
        request: Union[
            certificate_manager.CreateCertificateMapEntryRequest, dict
        ] = None,
        *,
        parent: str = None,
        certificate_map_entry: certificate_manager.CertificateMapEntry = None,
        certificate_map_entry_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a new CertificateMapEntry in a given project
        and location.


        .. code-block:: python

            from google.cloud import certificate_manager_v1

            def sample_create_certificate_map_entry():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                certificate_map_entry = certificate_manager_v1.CertificateMapEntry()
                certificate_map_entry.hostname = "hostname_value"

                request = certificate_manager_v1.CreateCertificateMapEntryRequest(
                    parent="parent_value",
                    certificate_map_entry_id="certificate_map_entry_id_value",
                    certificate_map_entry=certificate_map_entry,
                )

                # Make the request
                operation = client.create_certificate_map_entry(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.CreateCertificateMapEntryRequest, dict]):
                The request object. Request for the
                `CreateCertificateMapEntry` method.
            parent (:class:`str`):
                Required. The parent resource of the certificate map
                entry. Must be in the format
                ``projects/*/locations/*/certificateMaps/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            certificate_map_entry (:class:`google.cloud.certificate_manager_v1.types.CertificateMapEntry`):
                Required. A definition of the
                certificate map entry to create.

                This corresponds to the ``certificate_map_entry`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            certificate_map_entry_id (:class:`str`):
                Required. A user-provided name of the
                certificate map entry.

                This corresponds to the ``certificate_map_entry_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.certificate_manager_v1.types.CertificateMapEntry`
                Defines a certificate map entry.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [parent, certificate_map_entry, certificate_map_entry_id]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = certificate_manager.CreateCertificateMapEntryRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if certificate_map_entry is not None:
            request.certificate_map_entry = certificate_map_entry
        if certificate_map_entry_id is not None:
            request.certificate_map_entry_id = certificate_map_entry_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_certificate_map_entry,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            certificate_manager.CertificateMapEntry,
            metadata_type=certificate_manager.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def update_certificate_map_entry(
        self,
        request: Union[
            certificate_manager.UpdateCertificateMapEntryRequest, dict
        ] = None,
        *,
        certificate_map_entry: certificate_manager.CertificateMapEntry = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Updates a CertificateMapEntry.

        .. code-block:: python

            from google.cloud import certificate_manager_v1

            def sample_update_certificate_map_entry():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                certificate_map_entry = certificate_manager_v1.CertificateMapEntry()
                certificate_map_entry.hostname = "hostname_value"

                request = certificate_manager_v1.UpdateCertificateMapEntryRequest(
                    certificate_map_entry=certificate_map_entry,
                )

                # Make the request
                operation = client.update_certificate_map_entry(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.UpdateCertificateMapEntryRequest, dict]):
                The request object. Request for the
                `UpdateCertificateMapEntry` method.
            certificate_map_entry (:class:`google.cloud.certificate_manager_v1.types.CertificateMapEntry`):
                Required. A definition of the
                certificate map entry to create map
                entry.

                This corresponds to the ``certificate_map_entry`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. The update mask applies to the resource. For
                the ``FieldMask`` definition, see
                https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#fieldmask.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.certificate_manager_v1.types.CertificateMapEntry`
                Defines a certificate map entry.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([certificate_map_entry, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = certificate_manager.UpdateCertificateMapEntryRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if certificate_map_entry is not None:
            request.certificate_map_entry = certificate_map_entry
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_certificate_map_entry,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("certificate_map_entry.name", request.certificate_map_entry.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            certificate_manager.CertificateMapEntry,
            metadata_type=certificate_manager.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def delete_certificate_map_entry(
        self,
        request: Union[
            certificate_manager.DeleteCertificateMapEntryRequest, dict
        ] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deletes a single CertificateMapEntry.

        .. code-block:: python

            from google.cloud import certificate_manager_v1

            def sample_delete_certificate_map_entry():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                request = certificate_manager_v1.DeleteCertificateMapEntryRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_certificate_map_entry(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.DeleteCertificateMapEntryRequest, dict]):
                The request object. Request for the
                `DeleteCertificateMapEntry` method.
            name (:class:`str`):
                Required. A name of the certificate map entry to delete.
                Must be in the format
                ``projects/*/locations/*/certificateMaps/*/certificateMapEntries/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

                   The JSON representation for Empty is empty JSON
                   object {}.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = certificate_manager.DeleteCertificateMapEntryRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_certificate_map_entry,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=certificate_manager.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def list_dns_authorizations(
        self,
        request: Union[certificate_manager.ListDnsAuthorizationsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListDnsAuthorizationsAsyncPager:
        r"""Lists DnsAuthorizations in a given project and
        location.


        .. code-block:: python

            from google.cloud import certificate_manager_v1

            def sample_list_dns_authorizations():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                request = certificate_manager_v1.ListDnsAuthorizationsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_dns_authorizations(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.ListDnsAuthorizationsRequest, dict]):
                The request object. Request for the
                `ListDnsAuthorizations` method.
            parent (:class:`str`):
                Required. The project and location from which the dns
                authorizations should be listed, specified in the format
                ``projects/*/locations/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.certificate_manager_v1.services.certificate_manager.pagers.ListDnsAuthorizationsAsyncPager:
                Response for the ListDnsAuthorizations method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = certificate_manager.ListDnsAuthorizationsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_dns_authorizations,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListDnsAuthorizationsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_dns_authorization(
        self,
        request: Union[certificate_manager.GetDnsAuthorizationRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> certificate_manager.DnsAuthorization:
        r"""Gets details of a single DnsAuthorization.

        .. code-block:: python

            from google.cloud import certificate_manager_v1

            def sample_get_dns_authorization():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                request = certificate_manager_v1.GetDnsAuthorizationRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_dns_authorization(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.GetDnsAuthorizationRequest, dict]):
                The request object. Request for the
                `GetDnsAuthorization` method.
            name (:class:`str`):
                Required. A name of the dns authorization to describe.
                Must be in the format
                ``projects/*/locations/*/dnsAuthorizations/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.certificate_manager_v1.types.DnsAuthorization:
                A DnsAuthorization resource describes
                a way to perform domain authorization
                for certificate issuance.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = certificate_manager.GetDnsAuthorizationRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_dns_authorization,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def create_dns_authorization(
        self,
        request: Union[certificate_manager.CreateDnsAuthorizationRequest, dict] = None,
        *,
        parent: str = None,
        dns_authorization: certificate_manager.DnsAuthorization = None,
        dns_authorization_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a new DnsAuthorization in a given project and
        location.


        .. code-block:: python

            from google.cloud import certificate_manager_v1

            def sample_create_dns_authorization():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                dns_authorization = certificate_manager_v1.DnsAuthorization()
                dns_authorization.domain = "domain_value"

                request = certificate_manager_v1.CreateDnsAuthorizationRequest(
                    parent="parent_value",
                    dns_authorization_id="dns_authorization_id_value",
                    dns_authorization=dns_authorization,
                )

                # Make the request
                operation = client.create_dns_authorization(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.CreateDnsAuthorizationRequest, dict]):
                The request object. Request for the
                `CreateDnsAuthorization` method.
            parent (:class:`str`):
                Required. The parent resource of the dns authorization.
                Must be in the format ``projects/*/locations/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            dns_authorization (:class:`google.cloud.certificate_manager_v1.types.DnsAuthorization`):
                Required. A definition of the dns
                authorization to create.

                This corresponds to the ``dns_authorization`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            dns_authorization_id (:class:`str`):
                Required. A user-provided name of the
                dns authorization.

                This corresponds to the ``dns_authorization_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.certificate_manager_v1.types.DnsAuthorization` A DnsAuthorization resource describes a way to perform domain authorization
                   for certificate issuance.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, dns_authorization, dns_authorization_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = certificate_manager.CreateDnsAuthorizationRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if dns_authorization is not None:
            request.dns_authorization = dns_authorization
        if dns_authorization_id is not None:
            request.dns_authorization_id = dns_authorization_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_dns_authorization,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            certificate_manager.DnsAuthorization,
            metadata_type=certificate_manager.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def update_dns_authorization(
        self,
        request: Union[certificate_manager.UpdateDnsAuthorizationRequest, dict] = None,
        *,
        dns_authorization: certificate_manager.DnsAuthorization = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Updates a DnsAuthorization.

        .. code-block:: python

            from google.cloud import certificate_manager_v1

            def sample_update_dns_authorization():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                dns_authorization = certificate_manager_v1.DnsAuthorization()
                dns_authorization.domain = "domain_value"

                request = certificate_manager_v1.UpdateDnsAuthorizationRequest(
                    dns_authorization=dns_authorization,
                )

                # Make the request
                operation = client.update_dns_authorization(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.UpdateDnsAuthorizationRequest, dict]):
                The request object. Request for the
                `UpdateDnsAuthorization` method.
            dns_authorization (:class:`google.cloud.certificate_manager_v1.types.DnsAuthorization`):
                Required. A definition of the dns
                authorization to update.

                This corresponds to the ``dns_authorization`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. The update mask applies to the resource. For
                the ``FieldMask`` definition, see
                https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#fieldmask.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.certificate_manager_v1.types.DnsAuthorization` A DnsAuthorization resource describes a way to perform domain authorization
                   for certificate issuance.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([dns_authorization, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = certificate_manager.UpdateDnsAuthorizationRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if dns_authorization is not None:
            request.dns_authorization = dns_authorization
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_dns_authorization,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("dns_authorization.name", request.dns_authorization.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            certificate_manager.DnsAuthorization,
            metadata_type=certificate_manager.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def delete_dns_authorization(
        self,
        request: Union[certificate_manager.DeleteDnsAuthorizationRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deletes a single DnsAuthorization.

        .. code-block:: python

            from google.cloud import certificate_manager_v1

            def sample_delete_dns_authorization():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                request = certificate_manager_v1.DeleteDnsAuthorizationRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_dns_authorization(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.DeleteDnsAuthorizationRequest, dict]):
                The request object. Request for the
                `DeleteDnsAuthorization` method.
            name (:class:`str`):
                Required. A name of the dns authorization to delete.
                Must be in the format
                ``projects/*/locations/*/dnsAuthorizations/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

                   The JSON representation for Empty is empty JSON
                   object {}.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = certificate_manager.DeleteDnsAuthorizationRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_dns_authorization,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=certificate_manager.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-certificate-manager",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("CertificateManagerAsyncClient",)
