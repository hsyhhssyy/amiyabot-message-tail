import os
import types

from amiyabot import Message, Chain, log

from amiyabot.builtin.messageChain.element import Text
from core import AmiyaBotPluginInstance

curr_dir = os.path.dirname(__file__)

class  MessageTailPluginInstance(AmiyaBotPluginInstance):
    def load(self):
        # 将配置文件里的开关拧过来
        self.set_config('activate', False)

bot = MessageTailPluginInstance(
    name='消息小尾巴',
    version='1.0',
    plugin_id='amiyabot-message-tail',
    plugin_type='',
    description='在任何一条兔兔发送的消息后面加上小尾巴。',
    document=f'{curr_dir}/README.md',
    global_config_default=f'{curr_dir}/global_config_default.json',
    global_config_schema=f'{curr_dir}/global_config_schema.json',
)

old_message_func = {}

async def custom_send_chain_message(self, chain:Chain, use_http=False, *args, **kwargs):
    func = old_message_func.get(self)
    log.info(f'Created a new message with UUID: {chain.data.channel_id} {chain.data.user_id}')
    if bot:
        if bot.get_config('activate') == True:
            if bot.get_config('tail'):
                tail_text = bot.get_config('tail')
                # 如果chain.chain存在且最后一个类型是Text，则小尾巴要以换行开头
                if chain.chain and isinstance(chain.chain[-1], Text):
                    chain.text("\n")
                chain.text(tail_text)
    return await func(chain, use_http)


@bot.message_before_handle
async def _(data: Message, factory_name: str, instance):
    if instance not in old_message_func:
        old_message_func[instance] = instance.send_chain_message
        instance.send_chain_message = types.MethodType(
            custom_send_chain_message, instance)
