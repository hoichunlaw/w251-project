# Setup

## Start P100 VM

```
ibmcloud sl vs create --datacenter=lon06 --hostname=p100a --domain=dima.com --image=2263543 --billing=hourly  --network 1000 --key=1418191 --flavor AC1_8X60X100 --san
```