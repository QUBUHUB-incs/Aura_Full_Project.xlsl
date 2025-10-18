# Tunnel Sessions

## List Tunnel Sessions

List all online tunnel sessions running on this account.

### Request

GET /tunnel\_sessions

#### Example Request

```bash  theme={null}
curl \
-X GET \
-H "Authorization: Bearer {API_KEY}" \
-H "Ngrok-Version: 2" \
https://api.ngrok.com/tunnel_sessions
```

### Response

Returns a 200 response on success

#### Example Response

```json  theme={null}
{
  "next_page_uri": null,
  "tunnel_sessions": [
    {
      "agent_version": "3.1000.0-development",
      "credential": {
        "id": "cr_32ELG6KEtDBUO1jDXSqtOey4NgM",
        "uri": "https://api.ngrok.com/credentials/cr_32ELG6KEtDBUO1jDXSqtOey4NgM"
      },
      "id": "ts_32ELGMEqDFAlN8JoGk7mAGg7z6B",
      "ip": "10.110.2.2",
      "os": "linux",
      "region": "us",
      "started_at": "2025-09-04T10:11:27Z",
      "transport": "ngrok/2",
      "uri": "https://api.ngrok.com/tunnel_sessions/ts_32ELGMEqDFAlN8JoGk7mAGg7z6B"
    }
  ],
  "uri": "https://api.ngrok.com/tunnel_sessions"
}
```

#### Fields

| Name              | Type                                   | Description                                            |
| ----------------- | -------------------------------------- | ------------------------------------------------------ |
| `tunnel_sessions` | [TunnelSession](#tunnelsession-fields) | list of all tunnel sessions on this account            |
| `uri`             | string                                 | URI to the API resource of the tunnel session list     |
| `next_page_uri`   | string                                 | URI of the next page, or null if there is no next page |

#### TunnelSession fields

| Name            | Type               | Description                                                                                                                           |
| --------------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------- |
| `agent_version` | string             | version of the ngrok agent that started this ngrok tunnel session                                                                     |
| `credential`    | [Ref](#ref-fields) | reference to the tunnel credential or ssh credential used by the ngrok agent to start this tunnel session                             |
| `id`            | string             | unique tunnel session resource identifier                                                                                             |
| `ip`            | string             | source ip address of the tunnel session                                                                                               |
| `metadata`      | string             | arbitrary user-defined data specified in the metadata property in the ngrok configuration file. See the metadata configuration option |
| `os`            | string             | operating system of the host the ngrok agent is running on                                                                            |
| `region`        | string             | the ngrok region identifier in which this tunnel session was started                                                                  |
| `started_at`    | string             | time when the tunnel session first connected to the ngrok servers                                                                     |
| `transport`     | string             | the transport protocol used to start the tunnel session. Either `ngrok/v2` or `ssh`                                                   |
| `uri`           | string             | URI to the API resource of the tunnel session                                                                                         |

#### Ref fields

| Name  | Type   | Description                   |
| ----- | ------ | ----------------------------- |
| `id`  | string | a resource identifier         |
| `uri` | string | a uri for locating a resource |

## Get Tunnel Session

Get the detailed status of a tunnel session by ID

### Request

GET /tunnel\_sessions/\{id}

#### Example Request

```bash  theme={null}
curl \
-X GET \
-H "Authorization: Bearer {API_KEY}" \
-H "Ngrok-Version: 2" \
https://api.ngrok.com/tunnel_sessions/ts_32ELGMEqDFAlN8JoGk7mAGg7z6B
```

### Response

Returns a 200 response on success

#### Example Response

```json  theme={null}
{
  "agent_version": "3.1000.0-development",
  "credential": {
    "id": "cr_32ELG6KEtDBUO1jDXSqtOey4NgM",
    "uri": "https://api.ngrok.com/credentials/cr_32ELG6KEtDBUO1jDXSqtOey4NgM"
  },
  "id": "ts_32ELGMEqDFAlN8JoGk7mAGg7z6B",
  "ip": "10.110.2.2",
  "os": "linux",
  "region": "us",
  "started_at": "2025-09-04T10:11:27Z",
  "transport": "ngrok/2",
  "uri": "https://api.ngrok.com/tunnel_sessions/ts_32ELGMEqDFAlN8JoGk7mAGg7z6B"
}
```

#### Fields

| Name            | Type               | Description                                                                                                                           |
| --------------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------- |
| `agent_version` | string             | version of the ngrok agent that started this ngrok tunnel session                                                                     |
| `credential`    | [Ref](#ref-fields) | reference to the tunnel credential or ssh credential used by the ngrok agent to start this tunnel session                             |
| `id`            | string             | unique tunnel session resource identifier                                                                                             |
| `ip`            | string             | source ip address of the tunnel session                                                                                               |
| `metadata`      | string             | arbitrary user-defined data specified in the metadata property in the ngrok configuration file. See the metadata configuration option |
| `os`            | string             | operating system of the host the ngrok agent is running on                                                                            |
| `region`        | string             | the ngrok region identifier in which this tunnel session was started                                                                  |
| `started_at`    | string             | time when the tunnel session first connected to the ngrok servers                                                                     |
| `transport`     | string             | the transport protocol used to start the tunnel session. Either `ngrok/v2` or `ssh`                                                   |
| `uri`           | string             | URI to the API resource of the tunnel session                                                                                         |

#### Ref fields

| Name  | Type   | Description                   |
| ----- | ------ | ----------------------------- |
| `id`  | string | a resource identifier         |
| `uri` | string | a uri for locating a resource |

## Restart Tunnel Agent

Issues a command instructing the ngrok agent to restart. The agent restarts itself by calling exec() on platforms that support it. This operation is notably not supported on Windows. When an agent restarts, it reconnects with a new tunnel session ID.

### Request

POST /tunnel\_sessions/\{id}/restart

#### Example Request

```bash  theme={null}
curl \
-X POST \
-H "Authorization: Bearer {API_KEY}" \
-H "Content-Type: application/json" \
-H "Ngrok-Version: 2" \
-d '{}' \
https://api.ngrok.com/tunnel_sessions/ts_1vcl4fYZxXY0zNFbpCloylDCG0S/restart
```

#### Parameters

| Name | Type   | Description           |
| ---- | ------ | --------------------- |
| `id` | string | a resource identifier |

### Response

Returns a 204 response with no body on success

## Stop Tunnel Agent

Issues a command instructing the ngrok agent that started this tunnel session to exit.

### Request

POST /tunnel\_sessions/\{id}/stop

#### Example Request

```bash  theme={null}
curl \
-X POST \
-H "Authorization: Bearer {API_KEY}" \
-H "Content-Type: application/json" \
-H "Ngrok-Version: 2" \
-d '{}' \
https://api.ngrok.com/tunnel_sessions/ts_1vcl4fYZxXY0zNFbpCloylDCG0S/stop
```

#### Parameters

| Name | Type   | Description           |
| ---- | ------ | --------------------- |
| `id` | string | a resource identifier |

### Response

Returns a 204 response with no body on success

## Update Tunnel Agent

Issues a command instructing the ngrok agent to update itself to the latest version. After this call completes successfully, the ngrok agent will be in the update process. A caller should wait some amount of time to allow the update to complete (at least 10 seconds) before making a call to the Restart endpoint to request that the agent restart itself to start using the new code. This call will never update an ngrok agent to a new major version which could cause breaking compatibility issues. If you wish to update to a new major version, that must be done manually. Still, please be aware that updating your ngrok agent could break your integration. This call will fail in any of the following circumstances: there is no update available the ngrok agent's configuration disabled update checks the agent is currently in process of updating the agent has already successfully updated but has not yet been restarted

### Request

POST /tunnel\_sessions/\{id}/update

#### Example Request

```bash  theme={null}
curl \
-X POST \
-H "Authorization: Bearer {API_KEY}" \
-H "Content-Type: application/json" \
-H "Ngrok-Version: 2" \
-d '{}' \
https://api.ngrok.com/tunnel_sessions/ts_1vcl4fYZxXY0zNFbpCloylDCG0S/update
```

#### Parameters

| Name | Type   | Description |
| ---- | ------ | ----------- |
| `id` | string |             |

### Response

Returns a 204 response with no body on success
