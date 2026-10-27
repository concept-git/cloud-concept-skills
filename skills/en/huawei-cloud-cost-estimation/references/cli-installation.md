# KooCLI installation guide

> User instructions, not agent-executed setup. Installation, sudo, and download commands below are for the user to review and run locally. The agent may perform the read-only checks below; installation and credential configuration remain user actions.

## Readiness checks

1. Run `hcloud version` to confirm the CLI runs. For a requested connection check, inspect current `IAM KeystoneListAuthProjects --help`, then query with `--cli-region=cn-north-1 --cli-output=json`.
2. If configuration is missing, inspect `hcloud configure list` without exposing credentials or profile details, and ask the user to configure it locally. For permission errors, follow `iam-policies.md`.
3. Report the tested scope: CLI execution and, if successful, the current account's IAM project query. Do not infer BSS pricing or creation permissions. Do not use balances, bills, or an empty pricing request as a generic health probe.

## Overview

Huawei Cloud KooCLI (`hcloud`) is the unified Huawei Cloud CLI. Readiness checks are read-only; resource creation follows the separate provisioning workflow in `SKILL.md`.

After installation, run `hcloud version`. Obtain the latest package link from the official [quick installation guide](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html).

Official download location, in use since April 2026:

```text
https://cn-north-4-hdn-koocli.obs.cn-north-4.myhuaweicloud.com/cli/latest/
```

The old `hcloudcli.obs.cn-north-4.myhuaweicloud.com` domain and `hcloud_cli_*` package names are no longer valid.

## Script installation: Linux and macOS

The user must review and run these commands in their own terminal. Use the readiness checks above; the agent does not download or execute an installer.

```bash
BASE=https://cn-north-4-hdn-koocli.obs.cn-north-4.myhuaweicloud.com/cli/latest
curl -sSL "$BASE/hcloud_install.sh" -o ./hcloud_install.sh
# Review the script source and contents before running: less ./hcloud_install.sh
bash ./hcloud_install.sh
```

The default installation directory is `/usr/local/hcloud/`, with a link in `/usr/local/bin/`. For non-interactive installation after review:

```bash
BASE=https://cn-north-4-hdn-koocli.obs.cn-north-4.myhuaweicloud.com/cli/latest
curl -sSL "$BASE/hcloud_install.sh" -o ./hcloud_install.sh
# Review the script source and contents before running: less ./hcloud_install.sh
bash ./hcloud_install.sh -y
```

## Manual installation

### Linux AMD64

```bash
curl -LO "https://cn-north-4-hdn-koocli.obs.cn-north-4.myhuaweicloud.com/cli/latest/huaweicloud-cli-linux-amd64.tar.gz"
tar -zxvf huaweicloud-cli-linux-amd64.tar.gz
sudo mv hcloud /usr/local/bin/
hcloud version
```

### Linux ARM64

```bash
curl -LO "https://cn-north-4-hdn-koocli.obs.cn-north-4.myhuaweicloud.com/cli/latest/huaweicloud-cli-linux-arm64.tar.gz"
tar -zxvf huaweicloud-cli-linux-arm64.tar.gz
sudo mv hcloud /usr/local/bin/
hcloud version
```

### macOS AMD64

```bash
curl -LO "https://cn-north-4-hdn-koocli.obs.cn-north-4.myhuaweicloud.com/cli/latest/huaweicloud-cli-mac-amd64.tar.gz"
tar -zxvf huaweicloud-cli-mac-amd64.tar.gz
sudo mv hcloud /usr/local/bin/
hcloud version
```

### macOS ARM64

```bash
curl -LO "https://cn-north-4-hdn-koocli.obs.cn-north-4.myhuaweicloud.com/cli/latest/huaweicloud-cli-mac-arm64.tar.gz"
tar -zxvf huaweicloud-cli-mac-arm64.tar.gz
sudo mv hcloud /usr/local/bin/
hcloud version
```

### Windows 64-bit

```powershell
$url = "https://cn-north-4-hdn-koocli.obs.cn-north-4.myhuaweicloud.com/cli/latest/huaweicloud-cli-windows-amd64.zip"
Invoke-WebRequest -Uri $url -OutFile "huaweicloud-cli-windows-amd64.zip"
Expand-Archive -Path huaweicloud-cli-windows-amd64.zip -DestinationPath C:\hcloud
# Add C:\hcloud to the system Path, then run:
hcloud version
```

## Authentication

Prefer an existing local profile. Do not ask the user to paste an AK or SK into chat.

```bash
hcloud configure list
```

### Temporary environment variables

```bash
export HUAWEICLOUD_SDK_AK=<your-ak>
export HUAWEICLOUD_SDK_SK=<your-sk>
export HUAWEICLOUD_SDK_REGION=cn-north-1
```

Use only for explicitly authorized live verification. Clear these variables from that shell after verification.

### Interactive setup

If KooCLI has no configuration, the user can run this locally:

```bash
hcloud configure set
```

Do not pass plaintext AK/SK values through chat, script arguments, or logs.

### Verify configuration

```bash
hcloud configure list
# Expected shape:
# {
#   "current": "default",
#   "profiles": [{
#     "name": "default",
#     "mode": "AKSK",
#     "accessKeyId": "HPU****QBN",
#     "region": "cn-north-1"
#   }]
# }
```

## Obtain an AK/SK

1. Sign in to the [Huawei Cloud Console](https://console.huaweicloud.com).
2. Open the username menu and choose My Credentials.
3. Select Access Keys.
4. Choose Create Access Key.
5. Download the credential file and store it securely.

AK/SK values are long-lived account credentials. Do not store them as plaintext in code, configuration files, or conversations. Prefer IAM-user credentials over account-owner credentials, rotate them regularly, and grant least privilege. Live verification uses read-only BSS/API calls; do not execute payment, renewal, deletion, or modification commands.

## Troubleshooting

| Symptom | Cause | Action |
| --- | --- | --- |
| `hcloud: command not found` | Not on PATH | Place the executable in the intended PATH directory; for example `sudo mv hcloud /usr/local/bin/` |
| `Permission denied` | Executable permission missing | `chmod +x /usr/local/bin/hcloud` |
| Download returns 404 | Obsolete host or package name | Use the `cn-north-4-hdn-koocli` host and `huaweicloud-cli-*` packages |
| TLS certificate error | Outdated system CA certificates | Update the CA certificate package |
| Connection timeout | Network restrictions | Inspect proxy and firewall settings |

## References

- [Quick installation and downloads](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [Linux installation](https://support.huaweicloud.com/qs-hcli/hcli_02_003_02.html)
- [macOS installation](https://support.huaweicloud.com/qs-hcli/hcli_02_003_03.html)
- [Windows installation](https://support.huaweicloud.com/qs-hcli/hcli_02_003_01.html)
- [KooCLI product description](https://support.huaweicloud.com/productdesc-hcli/hcli_01.html)
- [API Explorer](https://console.huaweicloud.com/apiexplorer/#/openapi/overview)
- [IAM best practices](https://support.huaweicloud.com/bestpractice-iam/iam_0426.html)
