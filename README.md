# ReflectRPC

ReflectRPC is a Python library implementing a RPC client and server using the JSON-RPC 1.0 protocol. What sets it apart from most other such implementations is that it allows the client to get a comprehensive description of the functions exposed by the server. This includes type information of parameters and return values as well as human readable JavaDoc-like descriptions of all fields. To retrieve this information the client only has to call the special RPC function *\_\_describe\_functions* and it will get a data structure containing the whole description of all RPC functions provided by the server.

This ability to use reflection is utilized by the included JSON-RPC shell *rpcsh*. It can connect to every JSON-RPC server serving line terminated JSON-RPC 1.0 over a plain socket and can be used to call RPC functions on the server and display the results. If the server implements the *\_\_describe\_functions* interface it can also list all RPC functions provided by the server and show a description of the functions and their parameters.
