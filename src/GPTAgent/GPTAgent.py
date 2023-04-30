import openai # pip instal openai
import json

class GPTAgent:
    def __init__(self, name="", versao=3, reduzir=True, role=True, estilo="", limite_msgs=6, chat_key='./chat_key.json'):
        self.name = name
        self.models = ["","","","gpt-3.5-turbo", "gpt-4"]
        self.model = self.models[versao]

        self.com_role = role
        nomeando = ""
        if not self.name == "":
            nomeando = "Você é um assistente e seu nome é " + self.name + ". "
        self.role = nomeando + estilo
        self.role_message = {"role": "system", "content": self.role}
        self.messages = self.zerarRole(self.role)

        self.reduzir_buffer = reduzir
        self.limite_msgs = limite_msgs

        self.total_completions = 0
        self.total_prompts = 0
        self.total_tokens = 0
        self.total_messages = 0

        # Initialize the API key
        f = open(chat_key)
        chave = json.load(f)
        openai.api_key = chave['api_key']

    def perguntar(self, mensagem, append_msgs=True, reduzir_buffer=True, debug_gpt=False, only_system=False):
        if only_system:
            resposta, _ = self.__generate_answer(self.messages, debug_gpt)
        elif append_msgs:
            self.messages.append({"role": "user", "content": mensagem})
            resposta, _ = self.__generate_answer(self.messages, debug_gpt)
        else:
            resposta, _ = self.__generate_answer([{"role": "user", "content": mensagem}], debug_gpt)

        if append_msgs:
            self.messages.append({"role": "assistant", "content": resposta})
            if reduzir_buffer:
                self.messages = self.reduzir_buffer_mensagens(self.messages)

        return resposta

    def __generate_answer(self, messages, debug_gpt=False):
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                max_tokens=256,
                temperature=0.1,
                top_p=1,
                frequency_penalty=0.10,
                presence_penalty=0.10
            )

            if debug_gpt:
                print("DEBUG", messages)
                #print("DEBUG full response", response)
                print("DEBUG usage", response.usage)

            self.total_completions += int(response.usage.completion_tokens)
            self.total_prompts += int(response.usage.prompt_tokens)
            self.total_tokens += int(response.usage.total_tokens)
            self.total_messages += 1

            if debug_gpt:
                print("DEBUG Total Tokens", self.total_tokens, "Total completions", self.total_completions, "Prompts", self.total_prompts, "Messages", self.total_messages)

            return [response.choices[0].message.content, response.usage]
        except Exception as e:
            print("Deu ruim", e)
            return ["", ""]


    def zerarRole(self, role):
        self.role = role
        self.role_message = [{"role": "system", "content": role}]
        return self.role_message


    def reduzir_buffer_mensagens(self, mensagens):
        total_de_mensagens = len(mensagens)
        if total_de_mensagens >= self.limite_msgs:
            # o primeiro item da lista eh a regra, entao deleto o segundo (1)
            del mensagens[1]  # apaga um user
            del mensagens[1]  # apaga um assistant
        return mensagens