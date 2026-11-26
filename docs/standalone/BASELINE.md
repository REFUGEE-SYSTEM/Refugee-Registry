# Standalone Baseline Machine State

Recorded at: 2026-11-26T10:54:50+05:30

## docker ps -a
```
NAMES                                      IMAGE                                                   STATUS                        PORTS
openg2p-refugee-registry-celery-worker     openg2p-refugee-registry-celery:0.0.0-develop.716       Exited (0) 10 minutes ago     
openg2p-refugee-registry-celery-beat       openg2p-refugee-registry-celery:0.0.0-develop.716       Exited (0) 10 minutes ago     
openg2p-refugee-registry-staff-api         openg2p-refugee-registry-staff-api:0.0.0-develop.716    Exited (0) 10 minutes ago     
refugee-iam-staff-api                      openg2p/iam-staff-portal-api:1.3.0                      Exited (0) 10 minutes ago     
openg2p-refugee-registry-staff-ui          openg2p-farmer-custom-staff-ui:0.0.0-develop.716        Exited (0) 10 minutes ago     
openg2p-refugee-master-data-api            openg2p/master-data-api:develop                         Exited (0) 10 minutes ago     
refugee-awe                                openg2p/openg2p-awe:develop                             Exited (0) 10 minutes ago     
refugee-id-generator                       openg2p/openg2p-id-generator:1.0.0                      Exited (0) 10 minutes ago     
refugee-keycloak                           quay.io/keycloak/keycloak:26.0                          Exited (143) 10 minutes ago   
refugee-postgres                           postgres:16                                             Exited (0) 10 minutes ago     
refugee-redis                              redis:7-alpine                                          Exited (0) 10 minutes ago     
mds-standalone-api                         openg2p/master-data-api:develop                         Up 2 days (healthy)           0.0.0.0:8045->8000/tcp, [::]:8045->8000/tcp
mds-standalone-ui                          openg2p/master-data-ui:develop                          Up 2 days                     0.0.0.0:3005->3000/tcp, [::]:3005->3000/tcp
mds-standalone-db-seed                     openg2p/master-data-api:develop                         Created                       
mds-standalone-postgres                    postgres:16                                             Up 2 days (healthy)           0.0.0.0:5434->5432/tcp, [::]:5434->5432/tcp
mds-standalone-minio                       minio/minio:latest                                      Up 2 days                     0.0.0.0:9010->9000/tcp, [::]:9010->9000/tcp, 0.0.0.0:9011->9001/tcp, [::]:9011->9001/tcp
openg2p-livestock-registry-celery-worker   openg2p-livestock-registry-celery:1.2.2-rc.544          Exited (0) 10 minutes ago     
openg2p-dev-keycloak-proxy                 openg2p-dev-consent-stub:latest                         Exited (137) 10 minutes ago   
openg2p-dev-consent-stub                   openg2p-dev-consent-stub:latest                         Exited (0) 10 minutes ago     
openg2p-farmer-custom-partner-api          openg2p-farmer-custom-partner-api:0.0.0-develop.716     Exited (0) 10 minutes ago     
openg2p-livestock-registry-partner-api     openg2p-livestock-registry-partner-api:1.2.2-rc.544     Exited (0) 10 minutes ago     
openg2p-cropsown-registry-staff-api        openg2p-cropsown-registry-staff-api:0.0.0-develop.716   Exited (0) 10 minutes ago     
openg2p-cropsown-master-data-api           openg2p/master-data-api:develop                         Exited (0) 10 minutes ago     
openg2p-farmer-custom-staff-api            openg2p-farmer-custom-staff-api:0.0.0-develop.716       Exited (0) 10 minutes ago     
openg2p-farmer-custom-master-data-api      openg2p/master-data-api:develop                         Exited (0) 10 minutes ago     
openg2p-cropsown-registry-celery-worker    openg2p-cropsown-registry-celery:0.0.0-develop.716      Exited (0) 10 minutes ago     
openg2p-cropsown-registry-celery-beat      openg2p-cropsown-registry-celery:0.0.0-develop.716      Exited (0) 10 minutes ago     
openg2p-cropsown-registry-staff-ui         openg2p-cropsown-registry-staff-ui:0.0.0-develop.716    Exited (0) 10 minutes ago     
openg2p-postgres                           postgres:16                                             Exited (0) 10 minutes ago     
openg2p-redis                              redis:7-alpine                                          Exited (0) 10 minutes ago     
openg2p-farmer-custom-celery-beat          openg2p-farmer-custom-celery:0.0.0-develop.716          Exited (0) 10 minutes ago     
openg2p-farmer-custom-celery-worker        openg2p-farmer-custom-celery:0.0.0-develop.716          Exited (0) 10 minutes ago     
openg2p-farmer-custom-staff-ui             openg2p-farmer-custom-staff-ui:0.0.0-develop.716        Exited (0) 10 minutes ago     
openg2p-livestock-master-data-api          openg2p/master-data-api:develop                         Exited (0) 10 minutes ago     
openg2p-livestock-registry-celery-beat     openg2p-livestock-registry-celery:1.2.2-rc.544          Exited (0) 10 minutes ago     
openg2p-livestock-registry-staff-ui        openg2p-livestock-registry-staff-ui:1.2.2-rc.544        Exited (0) 10 minutes ago     
openg2p-livestock-registry-staff-api       openg2p-livestock-registry-staff-api:1.2.2-rc.544       Exited (0) 10 minutes ago     
openg2p-awe-api                            openg2p/openg2p-awe:develop                             Exited (0) 10 minutes ago     
openg2p-pbms                               openg2p/openg2p-pbms-core:develop                       Exited (2) 4 weeks ago        
openg2p-superset                           apache/superset:4.0.1                                   Exited (137) 10 minutes ago   
openg2p-staff-portal-ui                    openg2p/openg2p-staff-portal-ui:0.0.0-develop.54        Exited (0) 10 minutes ago     
openg2p-awe-ui                             openg2p/openg2p-awe-ui:develop                          Exited (0) 10 minutes ago     
openg2p-iam-staff-api                      openg2p/iam-staff-portal-api:1.3.0                      Exited (0) 10 minutes ago     
openg2p-id-generator                       openg2p/openg2p-id-generator:1.0.0                      Exited (0) 10 minutes ago     
openg2p-minio-init                         minio/mc:latest                                         Exited (0) 10 days ago        
openg2p-keycloak-init                      quay.io/keycloak/keycloak:26.0                          Exited (0) 10 days ago        
openg2p-minio                              minio/minio:latest                                      Exited (0) 10 minutes ago     
openg2p-keycloak                           quay.io/keycloak/keycloak:26.0                          Exited (143) 10 minutes ago   
central-nginx-1                            central-nginx                                           Up 3 days (healthy)           0.0.0.0:8081->80/tcp, [::]:8081->80/tcp, 0.0.0.0:7443->443/tcp, [::]:7443->443/tcp
central-service-1                          central-service                                         Up 3 days                     8383/tcp
central-enketo-1                           central-enketo                                          Up 3 days                     8005/tcp
central-postgres-1                         central-postgres                                        Exited (0) 6 weeks ago        
central-enketo_redis_main-1                redis:8.10.1                                            Up 3 days                     6379/tcp
central-enketo_redis_cache-1               redis:8.10.1                                            Up 3 days                     6379/tcp
central-postgres14-1                       central-postgres14                                      Up 3 days                     5432/tcp
central-secrets-1                          central-secrets                                         Exited (0) 6 weeks ago        
central-mail-1                             registry.gitlab.com/egos-tech/smtp:2.0.7                Up 3 days                     25/tcp
central-pyxform-1                          ghcr.io/getodk/pyxform-http:v4.5.0                      Up 3 days                     
livestock-db-seed-1                        5a2374700e2d                                            Exited (0) 8 weeks ago        
livestock-celery-beat-1                    94016e9842a0                                            Exited (0) 7 weeks ago        
livestock-celery-worker-1                  94016e9842a0                                            Exited (0) 7 weeks ago        
livestock-awe-ui-1                         4ba9b3dfebee                                            Exited (0) 7 weeks ago        
livestock-staff-api-1                      f2f51e7f7859                                            Exited (0) 7 weeks ago        
livestock-awe-1                            b88b96e301d1                                            Exited (0) 7 weeks ago        
livestock-sample-data-1                    5a2374700e2d                                            Exited (0) 8 weeks ago        
livestock-staff-ui-1                       81e18e6d529a                                            Exited (0) 7 weeks ago        
livestock-iam-register-1                   c1fe1679c34d                                            Exited (0) 8 weeks ago        
livestock-dashboard-ui-1                   1195823f32ef                                            Exited (0) 7 weeks ago        
livestock-registry-geo-seed                95206741a5b2                                            Exited (0) 8 weeks ago        
livestock-connector-worker-1               ee4f59ff0a9a                                            Exited (0) 7 weeks ago        
livestock-connector-ui-1                   27eb4c51e094                                            Exited (0) 7 weeks ago        
livestock-iam-1                            f0e5a149bcd5                                            Exited (0) 7 weeks ago        
livestock-partner-api-1                    358503293f7f                                            Exited (0) 7 weeks ago        
livestock-connector-api-1                  a2a7bf374549                                            Exited (143) 7 weeks ago      
livestock-keycloak-1                       ff02c932f024                                            Exited (143) 7 weeks ago      
livestock-minio-init-1                     a7fe349ef4bd                                            Exited (0) 8 weeks ago        
livestock-id-generator-1                   ce1ff61a8dbe                                            Exited (0) 7 weeks ago        
livestock-master-data-1                    fe153a0dea74                                            Exited (137) 7 weeks ago      
livestock-postgres-1                       95206741a5b2                                            Exited (0) 7 weeks ago        
livestock-redis-1                          ff02b58f971e                                            Exited (0) 7 weeks ago        
livestock-mailpit-1                        98b916bd3c8d                                            Exited (0) 7 weeks ago        
livestock-minio-1                          14cea493d9a3                                            Exited (0) 7 weeks ago        
frappe_docker_devcontainer-redis-cache-1   d146f83b1e0f                                            Exited (0) 6 months ago       
frappe_docker_devcontainer-redis-queue-1   d146f83b1e0f                                            Exited (0) 6 months ago       
frappe_docker_devcontainer-mariadb-1       78a5047d3ba3                                            Exited (0) 6 months ago       
frappe_docker_devcontainer-frappe-1        eb0df469589b                                            Exited (137) 6 months ago     
devcontainer-redis-queue-1                 d146f83b1e0f                                            Exited (0) 5 months ago       
devcontainer-redis-cache-1                 d146f83b1e0f                                            Exited (0) 5 months ago       
devcontainer-mariadb-1                     78a5047d3ba3                                            Exited (0) 5 months ago       
devcontainer-frappe-1                      fdadc40ae456                                            Exited (137) 5 months ago     
minio                                      14cea493d9a3                                            Exited (0) 6 months ago       
```

## docker volume ls
```
DRIVER    VOLUME NAME
local     0acd53e9c4af2da2508a33b397d1a65b50b4381ca8b65f65305d647512cda1dc
local     0c4464c541abdd38add879a31f11540ad5f60c3d7cf1926827152ff03cbc057e
local     2aaad4c0d6d84468febc8d0caf80137b59aa9d1b300cdc39cdfc778ac73dbf07
local     2d52dcf77a3fbf7e1dad9fe3c5b4f18d1f1587eff9f3fb8eb35e1fdc271023f2
local     2db747ae509b9379b55908ca7c044122b4f1c226493d165353a805913034d23c
local     2df9528fe275198bc216a1c74915606a2993b6feb2e9b8ddb6b7e540b0977925
local     2f89c00841161c75c109c990755eb506baa3f893a114c9e6d638eb515f13d276
local     02d39167857ddd54a849f8e27877c73efd69c97f98bdd621405fa2a858ea8cb0
local     3a69bb9bee5722c4d52fbfcc6586c11589567239c8187d71dad714f8c43a2af0
local     3c13cd3d06e5fd1e27933ec059238a5c8f29a59afade7fcbd68b1d24527080f0
local     3c3430598b2db5569cd9ba54d887bd4dd8183c069a3d911e426726eb5451c631
local     3f74390868cd71b959b6ce6907c1dde6978acd8e5fb48ba6a80654a22221f240
local     4a9a319bd10bb3db42ab0b40a9d8ffeaf52793322760d5ac6650a422cd16edf3
local     4af5a59c71ae6fdb05d34c661a0b9215bf8d095596102ac75e78a903d7192513
local     4c030c0672f756e4c3807b47cbe7b313b3f92cb4c2513ea26f153a0c80499bc3
local     4cca0005217ac1e000d048faba9249246774988f529e856c6c416615a63dbaf0
local     4da51c956c8c3d0e0fd736e05541a16308f12a608b529688ef75fc77a6dee347
local     4e5c25038634cb12cd65ecb077d5cfb193d795f3d3d212357d2954c47a14f649
local     4e48cf4c9bdb6d9bd998fae98e0dc68097cf4656543a58e6a3d39388ee537f55
local     4ed454748254a16bdd4051e8371268d9b40ef4ecebb052c643fa5c103e9b97f8
local     4f57c6b2da34c077b90d907cfc134df51ef4aa9fc76fb3b93ed2baa357bb023e
local     4f3066952cc1afe580c7b787fa3ecc1715fd59b289894a8e9079b722763123c6
local     4fb42a2ec050195e4e75b85390455997ba909553ee773caa9da014755fd0c68f
local     04bb26072790d2a99c984e0f8d446579df69498fa3049a804b65dad9b7620b91
local     6b98cb909f7b4cf27505d81f65170050a9f297b1593cb1366b6414956e839896
local     6cb97bacfa9f9f0ff7cf6ccef8a6f149042a7682d604ac318d37f4408f9b2673
local     06d1387116f74f0c2910f5325ace1dd59a5fb6e7b9d72fa162caa84b2458ef92
local     7ad2c1b603affd8e3eb324826f9d48856f5b36027dd2d676dc833288505236d4
local     7becc1dcbaf898ac58ee579cbd5a5786f715214900c850ad953ee4d38803d566
local     7d856fcb92de2750feff59507b21176fe03e126e19b0ab8097de9558ca9e75f7
local     07d677145b6e9fdc8ff9c03915212aaba3212bc2ef536db17294987d52e7896a
local     8e0d62d0afa51a644d1e0d79b86cf1d618b2f443bc47903d664a96753db1c7e3
local     8e528e7e8130545cf51cf42df55095fef30046da361630aeb0d8340a41180f2f
local     08b36472d79fcc8efe886cbdbae29f0e36726f86f148aaff8999f3a5a80dde78
local     9b5fc4fc64085aea8309cc49bdf85698de1f339c26bcb90cb3d96f1a2707592f
local     9d75139b5c03855632a99f21810e053ee3fc47e3d933c5a0ff3bdf321f1f197f
local     9f1b23d0c6e568baf864768ff400294824f7c2a2f184243a892a0a5800412618
local     9f5f81bd29a503a09d77c6feb6cccfb5559552b09bf7d67d44df0772cad1b0af
local     10bc419c3a28f66374b2e71f2b019a95337fb7679a1a83bf29bc6349090b11ee
local     12d578455d292373f88fa82c6d6a0fb264af5cd72cd1f7a301d968599299b185
local     027ef80d250fc4f87daaa441e4f792f11b57b13a989afeee47a49f98b7f84c50
local     33af8a787d2bf6ff6c02c4832362ee4477c527ab10a9aca5bb9a971f0af481c0
local     44b8e2146057750f84786aad859f27fa635c7e808c3449d1a8746ac12e96c3cd
local     45d502a8bdb808220dacfc9e7101abad0eb1d1e1700ab7ddcf3d7948dd90bb5e
local     46bb0ec664ac55a0a91684d42bdf0d0a577daa0b21629908d7ed5bdaddb4aae9
local     46fb0a324b749c4a76577f11ad66b12cb5aa671b1680cc0fbadeb3b28663a4ae
local     047f60b261be9161411467bfdfaa20f5013e13c3508bd97e3e94908695a19c41
local     50ba654c56b180f279ade854e41bbaa8d8d14bd6993d236032782ab3a990c5f4
local     60fa523e73495715c21d7d889a05252cfc066b805bdb18a7f03b09d135f1d038
local     64ba2ab8400e4ae9c28e89ec3248797a2768cea9a96133f9c882546ef58e5e92
local     74c4e26921662fd9bbbbb4a7d50cf5f29939e096194c860081493ed7cc8112dd
local     76c8f72f941f25be6908cde161f57869425df7e9544e9a878e0ba3b8261fcfe7
local     078ba3a4f684c65fe8ba256cf09f266eebe44b921767b225026c322a89ca11b1
local     87a902a606a9004886399ccbff312757ed5314f88d906d68f9439add3b2f89e0
local     87c363d0d6b6ab694f16113437397e5b7e1f64bb512e77e586a80d47df6ddbec
local     124fb189a98f7abc44c471f3cd590ea30016b378be3d889d1520c691596dc945
local     149f35f17580388a1e5464698cf18999e25a48ec381f5174a3a4c33b043c7478
local     219d41b0c6a05015ca67a251d183ddeb66cd0c862d7e7c5567becac2d0a3b8fe
local     0360cba8367e6a5741401e0d62c8118217727a57a4d01af7bcd5417a2c1b6457
local     366f556bff91c13f9fc0148ce1fd45ab5d38e72fccf0af06234e52ca14845fac
local     373c2ee5bea457944782514b73565b338e71340464beb55b7aa4046dff664f38
local     420abdc0d3262b301f26908c40509987dd1818569fe26f435538789a95f7b0e6
local     458a3452f45e5ea73af015d29c5a5dcf94ba8e72b538c99982751517b11b3cb7
local     522f829ff8ef5143b5953017f990f6c77001b1ddced19d51383f891cd4485a27
local     593aca27a2c395ea996dca72116680e67784be7ed5ec18622d8803096f04b088
local     668cb35b430fd9e8c6cab69c0342e450627d5d9f3fd4e6a02b83db934f155e02
local     834d0b8717cb850ab63a9b1582cc1b6bdcff41bda3dd45e992493d6a6f0ed10d
local     865fac8196bc4e95dc318b192afc09b9d9c3d3642daaee074b6d61b3b9cd2ff8
local     920ae3a0b22fdfd59fcce4b9676795cd49f2d12c96e830297ae2a793e88b7564
local     952dbcd5cd5060b817adca8c471c3caadf440031dd5d893392f5b3c375a4f7a7
local     2647ee5fa4b7c513d701d245596a7f63389336985883bf9d18b14c99bcd6d8fe
local     3044db9e3d031f32f6b10f3f100f11ffc94e482484bc1419570b05d8c1347eb5
local     3218a721bdce8f98bfb346411e1c2dd2bc9c80ef0146c199d984f317acd8d51f
local     03282a66c1e05f5dd747939681902a52b932ef2d1c91b8b4aa02ee8ba0a72602
local     3737a7fc6a9dd68d3bb26afdc80ee37226031822aef733487b247973ae59fa2c
local     3815a1eb555e6a0cc07fd378962a0888786ebadfe06df0272cc1ce62be1170b7
local     4192f79eb61f0494032374cc4c511555ac20de90020e7189b4474f14493c6d15
local     5038f5f7df211b87e95a913e20ad36508036b3ceaac195c7bf85dbaa8af2671f
local     7808ee8e2d4b8e18d25227f8dd544a335d48c51d7e4ac5549c52b23cf604a8d3
local     8834da403dd70a54089898b4f793b86824486340fae1119f783820095f963801
local     9232ddb9621f192a618d19ced34613dbd0424b4a243b54e288e9d1ededc1d63d
local     9704ceb90e3dd545949369d7d8c0d66e0c65faae53ec85418b50fe3e8d87131b
local     014753f32b586af6479976245dbccfb92786a1d3b2f472caeb894f400807a4a5
local     34727fcb17bdadce70256fb279cb46752701e220b68d210b3fe7516aaf328d06
local     70726cec1269d4e1dc4ef226cfb55c6547d0d74785427097b65d07eeda8e8c52
local     174213b02be46f70bcc1108a221dd99d049b9717ef17921daa35d57eba613776
local     282095acf4340a59e70f25255827f5df2e9ac5e589627d0e3829412fd263fa47
local     695514c4c87fce6603834ea227cb54d965693cea8311f6cb01ea80d5cd8738ce
local     731212b8a55d3addd609e5b14e1e83166353d08144b9ec2af40aef5064e0af3e
local     857003fe4a57b3eaba9032203ca124361f3482f410c3f740279704b343629d34
local     875444cd1cd58f37e6554b22f6fdb6e84b67838a2b0c3a5e07d0a53d3f882e3f
local     967664fc896d88f9f92c40877a6d26b84b21cf7391b5051e64f3614588e3a473
local     4863697dd6b7487b3a9772f99f28446b174c772dcc735c6504e411337d54ac92
local     7702600b4e28e62c9e35011eb71e4921c96d9ddd166564d70389b0551dce094e
local     8081016e3c6e4406a6afa4deda4f00508775556f9901060bc3617d8ec307395c
local     95601613a078df665f7c0c55a784dac55934d9af1845bbb11af528dc10791ba5
local     97996477d6a2ab4190bd73c7ff1dc96c2144d9f9d1bcc06323c0ff9df91a7659
local     958353357b12227f4209af298cab337c42ba4a0a210f0d307422940b81acf877
local     03958546723a7148a75a36815df258f7f736d676537ac5b4a38a982d8c29ef55
local     93943937962c93568c6ee5f96954ddc300e69092fbcdb88fae152d3fba412fbc
local     a4ebb25af40452e1ddf572f863843f130dc29e1f3fb56b2b448e38aedcd28973
local     a5d790f5b7b624957cfc569a9942bdd09c9b243bfd434ecd080dc74a445edcf8
local     a73c297b6c0d2983644768c8935bc419677265e4a6a317c62bffbaad3260f350
local     a75ca99d33b0d158a9db4bf7a39db8fd9b854ed21bcb49bf2b7b1a1b8d2771fc
local     a298c98b8748b8e11411d2ddd19aea94399d80bc3e6c35b550236c5afc886032
local     ac7d939360f2edbfce492399605a30703402fb99840b067e46b2b7c81c88433a
local     ad3f50bbbee0eed46a15f911e72008a20a42e060278e860c610293132507ddc3
local     adccf798a9fa46d10cc97d8d0df81af2ab0f1c3b27a31fd3cf035a47d2fcca52
local     af65e19d4f7116ba34e1c3e7b882897816c2663b2b43756d1a1d072bfd1ff707
local     b26d275f44725f95be42735f525b249d535fef67dfccfca62ed6903f313a1a55
local     b513ccb520c2f0d1b6f83315e9e03f22090ae0ca26c02171feba2833b7994119
local     b6590caf2af8411cdfb58773dbdf4ec6f6dc5436d24ee38888f9dc16b4f643f3
local     b51365fb05638f1a477afae509b4fe51e6d333d9d8a5913762affab3ad546357
local     b102963f1cf3261ac5020ca3d1a0cc0286118c4dfa5f14638942a0109ab6a8f3
local     be44eb80517715f6e5f6cddff8129f8829f280a53e983e984465e171f46a09a9
local     bf688adf2c12dcdcf8a11696c41aba54295642cfd1eaa885866cbea7c12bc7a3
local     c0dc75c9355780ed0a62c3b27d98438bd654e4552d08bb640ca5455ae3cb8e68
local     c4d6337f5128c50ea399ebafa2a67bb1d4688f9983e3b2223b2b14f125683f11
local     c10e8fe813d8eafd7aa57f2d6b11ed2112a95826d0c2e2ae38c13ca865910437
local     c80ffdb0935a6ad83a6b5cee3c65816e4c910e2909f2009927cb1ca27278eb86
local     c82b86d6ee6cf2a11d81080f8bfdd7c5d75731c045d8c42be9afc6b8011f903a
local     c3249d9cb35feda88369526c80961ea29c32b816caf3c67e72f9e164a51756d6
local     c651149274671b12a9109b6dbfdbc2121364f31c2b8eea1319ef6233bc9c04d6
local     ca3add3a55be2140e5a179141af4d39b1f36362a257b3614ae9ce2f94301d517
local     ce9e42022a9814aa3b6e061299b3603bbf5132c41378bfca4970c41295335c95
local     cecaf6cebc59aff3f797a1c257af4ee46ccc410c3d0e6694c8072a8898ebd9fb
local     central_enketo_redis_cache
local     central_enketo_redis_main
local     central_postgres14
local     central_secrets
local     cf6b1d7af1e8d2fa9d7f5dbb6c3069a0858d9a6271fa8747f2ef95a7db0fae2f
local     d5a84a1340aa233f32f66ba99ed20af7ca07e7eb93e0c2495e3430a971b424de
local     d39f254ab5e56678b4bc7c48aaa03a201ebe9d364d9a07f86c3504087a9b4c30
local     d44efe8920446de0bb9d83843601b2d669ebc45f503c18b1a6f432ecb9d7716f
local     d0048f11a31cfaba7aeb30bb5279acc2a97950d3ae9cd6bd265475e2564eff29
local     d83b705dfe5c5fb2f0e79765ef90b05394bc207b846777b688b32c504e056466
local     da8d5d26c47a97ab4760a2707b05e9941b3921f5815f643ee3fbb9eadbda9ce2
local     dab2d4beb178b2b9a3115eec4ef3e92814864a3f410c932388a7be63f2a8c9b2
local     dd0eb48a50b87ab717f2631ecd3edb79d99d78f824970a0c68c309bdae6e2ef7
local     dd2ca746de8306713255bb0b8f091fb7c5c5585abe0a90751c3adc49c01f8f92
local     ddcf62b470c627e4c0fe081e8b8a864fd0c28256dd613222d4d9c86f09803b72
local     devcontainer_mariadb-data
local     e0a5aa691ea49580ccb19dc5eb0779ee7acd893e3d248cde1a440fe4d33b7bba
local     e1dad41ab1a18369ff46f9516357259a988bc27113d7691c3e51bae79cbe2f24
local     e3b8209cf6746263719df41fe76ae55d9996e5bccba2cc33741f7bd8e7644be9
local     e3ca71a12319f5ea37c61113826457169eed7fdefd3072b67172d8ad01597a26
local     e5d4bf7c5e410598dd47170993573761fe84d122764b3e7c335eb4ab78fa8c03
local     e6e7df44e1510f2f0ca546a51e6687c4c59b8162aa4727f1bcad1dd4dc8676be
local     e8c516ec5960b1f7d0a25f6c2d491792d6771115eadccd2a69f63543a1859874
local     e44cf29e02c183b2ea065997346eac66acb35a6d4146b97b6bce41de18102cea
local     e445ee5df76c576d7a8539183333f7c9f4b62e52c55e9bc4490c55793acc61ef
local     e822b9c1e9a65e9ce954a2cd5aeb43288a72b3e5b1edcbd52448ac1dd5a3e0cf
local     e1363e1b5e176cd9858b14115cb34b38415b0b5835773e632d4ddbe778487298
local     ea9d28a2d1b2a26858b30f56a89b508b4bd5681cf73748ab78d20f265f89a298
local     ebb496b600f9b7425e040805e17c0cd049040eb4b7ac984ffea48c74a3d7c843
local     ec70ecbb7acb458dfc7d67acaffde5474f2b09be435fca57fa752f7638ebf22d
local     ec236fe253d3ca4f9b85d4d1db893834efcd0460db96ef77ebf603a94bfd59eb
local     ecbeff69902aa7c7aea8acc35be9c0e486e6c2ede691585888e40f3f1ec1062f
local     ed2687ba50de0e82940cb2ce68f9481617a26ba9b5c60efc4508fc57fbfc79c9
local     edbad02a65df42682847ceebd7de55d97c6558ac17126a2e232dcdd3dceb4f4c
local     f3ec3f73d6842555dca7eb13ea53d194c8a027ebb8fe262a67c4c43fb3f20fd6
local     f04df0684a062b7ade14bb71ccd168adfc894a354e34e9b4f6395cbcfa3e9858
local     f5a0fadc119d71e4b32972db8a7f7096afde945b213600ddc15758bf6f236ac7
local     f9f8ffa48fd2059c6f83b0c8c0760358614c0b1b25ea63b422a20173314406ba
local     fa1ce31514ba2486ce682cef4d411924b8173cc55cde66fc10017bbed5018618
local     fa16ab63ea69cc580d37cd4621d8be4694bb5ca1aa34b8ed36d2a0691810ae66
local     fbc8391702e50998ee1b91fac5fbd3d5be35b1fcdfa21895e47d7350f1691862
local     fc9bc0f70b3f81c3731c1d0f8426b43b9a444cc3d0e0586654b598894b389ace
local     fd8a88e2ea8d41fc5e82ddeb07d9487d7b06701155a90b45ac656d6867b7bc19
local     fdcf32218a03465de69484bbce0ca5225dd7b182aff3b22f86807e937901fff4
local     fe4a6d1d2d41a2b10bff43f9fca8076c60de7105ce24aad63d80b105f1efc1a0
local     frappe_docker_devcontainer_mariadb-data
local     livestock_minio-data
local     livestock_postgres-data
local     mds_mds_miniodata
local     mds_mds_pgdata
local     openg2p-developer_minio_data
local     openg2p-developer_postgres_data
local     openg2p-developer_refugee_postgres_data
local     openg2p-developer_superset_home
```

## docker network ls
```
NETWORK ID     NAME                                 DRIVER    SCOPE
40e757558379   bridge                               bridge    local
ea3e71f0e98d   central_default                      bridge    local
f3d33b33482a   devcontainer_default                 bridge    local
36a43b0c6a83   frappe_docker_devcontainer_default   bridge    local
3f6ef67224f2   host                                 host      local
d51e6ab3e807   livestock_default                    bridge    local
bf2bae46fdba   mds_mds_net                          bridge    local
cc503d43b550   none                                 null      local
679fca352619   openg2p-developer_default            bridge    local
```

## ss -ltn
```
State  Recv-Q Send-Q                               Local Address:Port  Peer Address:PortProcess
LISTEN 0      10                                      172.21.0.1:56769      0.0.0.0:*          
LISTEN 0      511                                      127.0.0.1:6379       0.0.0.0:*          
LISTEN 0      10                                      172.22.0.1:54265      0.0.0.0:*          
LISTEN 0      4096                                 127.0.0.53%lo:53         0.0.0.0:*          
LISTEN 0      4096                                       0.0.0.0:3005       0.0.0.0:*          
LISTEN 0      4096                                       0.0.0.0:22         0.0.0.0:*          
LISTEN 0      511                                        0.0.0.0:80         0.0.0.0:*          
LISTEN 0      10                                      172.19.0.1:54273      0.0.0.0:*          
LISTEN 0      4096                                     127.0.0.1:38661      0.0.0.0:*          
LISTEN 0      10                                      172.17.0.1:47230      0.0.0.0:*          
LISTEN 0      4096                                     127.0.0.1:37913      0.0.0.0:*          
LISTEN 0      200                                      127.0.0.1:5432       0.0.0.0:*          
LISTEN 0      4096                                       0.0.0.0:7443       0.0.0.0:*          
LISTEN 0      4096                                       0.0.0.0:8045       0.0.0.0:*          
LISTEN 0      4096                                       0.0.0.0:8081       0.0.0.0:*          
LISTEN 0      10                                   192.168.0.127:46562      0.0.0.0:*          
LISTEN 0      80                                       127.0.0.1:3306       0.0.0.0:*          
LISTEN 0      4096                                     127.0.0.1:631        0.0.0.0:*          
LISTEN 0      4096                                       0.0.0.0:5434       0.0.0.0:*          
LISTEN 0      10                                      172.20.0.1:34315      0.0.0.0:*          
LISTEN 0      4096                                       0.0.0.0:9010       0.0.0.0:*          
LISTEN 0      4096                                       0.0.0.0:9011       0.0.0.0:*          
LISTEN 0      10                                      172.18.0.1:48683      0.0.0.0:*          
LISTEN 0      4096                                    127.0.0.54:53         0.0.0.0:*          
LISTEN 0      10                                       127.0.0.1:42692      0.0.0.0:*          
LISTEN 0      511                                      127.0.0.1:42607      0.0.0.0:*          
LISTEN 0      10                                      172.23.0.1:40034      0.0.0.0:*          
LISTEN 0      10         [fe80::2c52:3dff:feb7:a24a]%vetha389462:42355         [::]:*          
LISTEN 0      10         [fe80::684a:73ff:fe44:576f]%veth64db102:48104         [::]:*          
LISTEN 0      10         [fe80::c052:34ff:fe34:1fff]%veth7308596:42760         [::]:*          
LISTEN 0      10             [fe80::90b5:5fff:fe1c:166a]%docker0:34458         [::]:*          
LISTEN 0      4096                                          [::]:3005          [::]:*          
LISTEN 0      4096                                          [::]:22            [::]:*          
LISTEN 0      511                                           [::]:80            [::]:*          
LISTEN 0      10                                           [::1]:60735         [::]:*          
LISTEN 0      4096                                          [::]:7443          [::]:*          
LISTEN 0      4096                                          [::]:8045          [::]:*          
LISTEN 0      4096                                          [::]:8081          [::]:*          
LISTEN 0      4096                                          [::]:5434          [::]:*          
LISTEN 0      10         [fe80::90a4:5eff:fee3:7aba]%vethc3029c8:59553         [::]:*          
LISTEN 0      4096                                         [::1]:631           [::]:*          
LISTEN 0      10           [fe80::7167:e72b:7473:d0bd]%wlp0s20f3:33683         [::]:*          
LISTEN 0      10          [fe80::8cac:8dff:fe6d:367]%vethddda990:51659         [::]:*          
LISTEN 0      10         [fe80::f835:18ff:febc:8d01]%veth6eaa5c3:55026         [::]:*          
LISTEN 0      10     [fe80::a4ae:c7ff:fe5e:2622]%br-ea3e71f0e98d:32841         [::]:*          
LISTEN 0      10         [fe80::3cc5:88ff:feed:65f8]%veth309dcdb:59278         [::]:*          
LISTEN 0      4096                            [::ffff:127.0.0.1]:63342            *:*          
LISTEN 0      10     [fe80::e03b:4cff:feb8:2df1]%br-679fca352619:43242         [::]:*          
LISTEN 0      10         [fe80::b87c:ceff:fee4:fe15]%veth0628d89:48670         [::]:*          
LISTEN 0      4096                                          [::]:9010          [::]:*          
LISTEN 0      4096                                          [::]:9011          [::]:*          
LISTEN 0      10         [fe80::a00c:dbff:fe86:e32e]%veth7ac92b2:43353         [::]:*          
LISTEN 0      10         [fe80::78f2:81ff:fe6d:a264]%vetha74b696:48757         [::]:*          
LISTEN 0      10          [fe80::7cc5:fff:fe23:3944]%veth6717704:39777         [::]:*          
LISTEN 0      10     [fe80::8ca2:6cff:fe7c:46bb]%br-bf2bae46fdba:40427         [::]:*          
LISTEN 0      511                                          [::1]:6379          [::]:*          
LISTEN 0      10         [fe80::b09a:acff:fe95:f756]%vethc336824:49932         [::]:*          
```
