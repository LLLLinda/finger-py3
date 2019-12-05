# finger-py3
4651 serverless implementation

作業系統使用 [ubuntu 18.04](http://releases.ubuntu.com/18.04/)。安裝完使用以下指令更新 OS。

```shellscrupt
$ sudo apt-get update && sudo apt-get dist-upgrade
```

OpenFaaS 使用 Container 提供 function 運行環境，底層可透過 [Docker Swram](https://docs.docker.com/engine/swarm/swarm-tutorial/create-swarm/) 或 [Google Kubernetes](https://kubernetes.io/) 來延伸資源規模。

本文為一個快速導引，使用 Docker Swarm 來快速建置 OpenFaaS 所需的 Container 環境。

Docker 安裝很簡單，只需:

```shellscrupt
$ wget -O - https://get.docker.com | sudo bash
```
再去泡杯茶 :tea:

Docker安裝完，可以使用以下指令，將 linux 的使用者 (user) 加入 docker group，這樣一來，不用 root 權限即可以使用 Docker。

```
$ sudo usermod -aG docker YOUR_USER_NAME
```

接下建置 docker swarm

```
$ docker swarm init
Swarm initialized: current node (kl74eq0mwhm03xtt8c6m95253) is now a manager.

To add a worker to this swarm, run the following command:

    docker swarm join --token SWMTKN-1-4m0wb27fsf8wsvfzrz60cjiuumkojzf3dbcn29vj7dufz9bevv-bezhrnutrcbmnbwk16xcafo9h 192.168.64.129:2377

To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
```

本文只使用一台VM，身兼 manager & worker。若環境中有多台機器，可以登入到其他機器，並使用上述的 docker swarm join --token xxxx，讓加入更多機器。

完成後，執行 "docker node ls"，看到以下畫面，就表示可以繼續下一步驟。

```
docker node ls
ID                            HOSTNAME            STATUS              AVAILABILITY        MANAGER STATUS
kl74eq0mwhm03xtt8c6m95253 *   ubuntu              Ready               Active              Leader
```
## 部署 OpenFaaS

執行以下指令，會自動部署 OpenFaaS。 (過程需要 git，可以使用 sudo apt-get install git 安裝)

```
$ cd ~
$ git clone https://github.com/alexellis/faas/ && cd faas
$ ./deploy_stack.sh
```

使用瀏覽器，打開 http://your_host_ip:8080/ 就會看到 OpenFaaS Portal 

為了後續建置 function，還需要安裝 faas-cli。安裝方式還是很簡單:

```
$ curl -sSL https://cli.openfaas.com | sudo sh
x86_64
Getting package https://github.com/openfaas/faas-cli/releases/download/0.5.0/faas-cli
Attemping to move faas-cli to /usr/local/bin
New version of faas-cli installed to /usr/local/bin
Creating alias 'faas' for 'faas-cli'.
```

run simple redis server
```
$ bash scripts/bootstrap.sh latest
$ git clone https://github.com/thomasjpfan/redis-cluster-docker-swarm.git
$ cd redis-cluster-docker-swarm/
$ bash scripts/bootstrap.sh latest
$ docker run --rm --network func_functions -ti redis:4.0.11-alpine redis-cli -h redis

```


download finger game source code
```
$ git clone https://github.com/LLLLinda/finger-py3.git
```


資料夾，會發現產生了兩個目錄，兩個檔案。其中 template 為樣本庫，暫時先不討論它。
我們直接來看:
```
finger-py3.yml  # function 相關屬性
finger-py3\handler.py # 實作程式碼的地方
finger-py3\requirements.txt # 若需要 python third-package，填入此處
```

建置 function
```
$ faas-cli build -f finger-py3.yml
$ faas-cli build -f redis-fn.yml
$ faas-cli build -f one-process.yml
```

## 執行 Function
讓我們來測試這個 otp服務。

測試前，需要先將部署 function。(記得加入 --gateway，來指定 Gateway，並將 "192.168.64.129" 改為實際 IP

```
$ faas-cli deploy -f finger-py3.yml --gateway http://192.168.64.129:8080
$ faas-cli deploy -f redis-fn.yml --gateway http://192.168.64.129:8080
$ faas-cli deploy -f one-process.yml --gateway http://192.168.64.129:8080
```

先用 curl 測試， '-d "jess"' 表示要產生哪一位使用者的 otp
```
$ curl -XPOST 192.168.64.129:8080/function/finger-py3 -d "1111"
$ curl -XPOST 192.168.64.129:8080/function/redis-fn -d "{\"playername\":\"zoe\",\"current_stat\":\"1111\"}"
$ curl -XPOST 192.168.64.129:8080/function/finger-py3 -d "1111"
```

回到 OpenFaaS Portal，會看到 functions 已經在列表上。請依照下圖步驟，逐一輸入執行。步驟3，即是發出 request，步驟4即是回傳值。

## 觀察監控數據

OpenFaaS 使用 [Prometheus](https://prometheus.io/) 進行監控數據的採集。

使用瀏覽器，打開 http://your_host_ip:9090/

就會看到 Prometheus，切換到 Graph Tab，可以輸入條件並產生圖表



## 參考資料

* [Your first serverless Python function with OpenFaaS](https://blog.alexellis.io/first-faas-python-function/)
* [Redis cluster cache configuration for docker swarm](https://github.com/thomasjpfan/redis-cluster-docker-swarm)
