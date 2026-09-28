PROVIDERS = {
    "deepseek":{
        "base_url": "https://api.deepseek.com",
        "api_key_env": "DEEPSEEK_API_KEY",
        "default_model": "deepseek-v4-flash",
    },
    "zhipu":{
        "base_url": "https://open.bigmodel.cn/api/paas/v4",
        "api_key_env": "ZHIPU_API_KEY",
        "default_model": "glm-5.3-flash",
    },
}

DEFAULT_PROVIDER = "zhipu"