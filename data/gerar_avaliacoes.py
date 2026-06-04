"""
Gera avaliacoes.csv com reviews diversas e realistas em pt-BR.
Mantém compatibilidade com a estrutura original.
"""

import random
import pandas as pd
from datetime import datetime, timedelta

random.seed(42)

# Templates por nota (1-5), organizados por tema
REVIEWS = {
    1: [
        "Comida chegou completamente fria, parece que ficou parada horas.",
        "Pedido errado, recebi prato diferente do que pedi.",
        "Embalagem rasgada, comida derramou toda na sacola.",
        "Entrega levou mais de 2 horas. Absurdo!",
        "Comida com gosto estranho, suspeito que estava estragada.",
        "Faltaram itens no pedido. Paguei por algo que não veio.",
        "Molho derramado, embalagem completamente inadequada.",
        "Entregador sumiu com o pedido. Tive que acionar o suporte.",
        "Carne crua por dentro. Totalmente inaceitável.",
        "Errou o endereço, comida foi entregue no vizinho.",
        "Arroz empapado e feijão aguado. Parece sobra do dia anterior.",
        "Lanche amassado, batata frita encharcada de óleo.",
        "Pedi sem cebola por alergia. Veio com cebola. Problema sério.",
        "Pizza chegou fria e murcha. Parecia papelão.",
        "Sopa derramada na embalagem, completamente fria ao chegar.",
        "Entregador rude e pedido incompleto. Pior experiência.",
        "Comida com cabelo. Não aceitarei mais pedidos desse restaurante.",
        "Prazo era 40 min, levou 2h30. Comida obviamente fria.",
        "Embalagem inadequada para frango assado. Chegou encharcado.",
        "Cobrou a mais e o pedido veio incompleto.",
    ],
    2: [
        "Entrega atrasou bastante e a comida chegou morna.",
        "Sabor razoável, mas a porção foi bem menor que o esperado.",
        "Embalagem simples demais, comida misturou tudo.",
        "Demorou mais que o prometido e o preço não justifica.",
        "Comida ok mas fria. Precisa melhorar na entrega.",
        "Pedido correto, mas qualidade abaixo do esperado pelo preço.",
        "Frango ressecado, parecia requentado.",
        "Molho faltando, pedi extra e não veio.",
        "Entrega foi lenta, embalagem estava úmida.",
        "Sabor mediano, já comi muito melhor no mesmo estilo.",
        "Porção pequena para o preço. Fiquei com fome.",
        "Atendimento via chat demorou muito para responder.",
        "Pizza com massa crua no meio. Precisava de mais tempo no forno.",
        "Comida chegou em temperatura morna, não quente.",
        "Itens básicos faltando, como guardanapo e talheres.",
        "Embalagem de salada amassada, folhas murchas.",
        "Pedido atrasou 45 minutos além do prometido.",
        "Refrigerante chegou quente, sem gelo nenhum.",
        "Pão do lanche estava duro, como se fosse de ontem.",
        "Qualidade caiu muito comparado ao que era antes.",
    ],
    3: [
        "Ok para o dia a dia, nada especial.",
        "Pedido correto, sabor mediano. Pode melhorar.",
        "Entrega dentro do prazo, comida ok. Nada extraordinário.",
        "Tudo certo, sem reclamações. Só não ficou surpreso.",
        "Razoável pelo preço. Já comi melhor, já comi pior.",
        "Boa comida mas embalagem simples. Cumpriu o prometido.",
        "Chegou no prazo, sabor satisfatório.",
        "Porção adequada, sabor regular.",
        "Nada impressionante, mas também não decepciona.",
        "Preço justo para o que oferece.",
        "Entrega rápida, mas a comida era comum.",
        "Sabor agradável, porém a porção poderia ser maior.",
        "Embalagem funcional, comida na temperatura certa.",
        "Restaurante cumpriu o básico esperado.",
        "Prato bem montado, sabor dentro do esperado.",
        "Não voltarei toda semana, mas posso pedir de vez em quando.",
        "Atendimento neutro, comida sem destaque.",
        "Para saciar a fome cumpre o papel, mas não é destaque.",
        "Pedido chegou completo, qualidade regular.",
        "Comida caseira simples. Sem inovação, mas honesta.",
        "Tempo de espera razoável para a região.",
        "Frango grelhado sem tempero marcante.",
        "Salada fresca mas molho muito ácido.",
        "Massa al dente mas molho podia ter mais sabor.",
    ],
    4: [
        "Comida saborosa e entrega dentro do prazo. Recomendo.",
        "Entrega rápida e comida saborosa, 10/10!",
        "Adorei! Já virou meu favorito.",
        "Comida incrível, super recomendo!",
        "Atendimento excelente e embalagem cuidadosa.",
        "Sabor excelente e porção generosa.",
        "Entrega antes do prazo e tudo bem embalado.",
        "Qualidade consistente. Sempre bom ao pedir.",
        "Frango grelhado perfeitamente temperado.",
        "Pizza crocante e bem distribuída. Parabéns ao restaurante.",
        "Embalagem térmica manteve a comida quente.",
        "Prato caprichado, ingredientes frescos e saborosos.",
        "Preço justo para a qualidade entregue.",
        "Entregador simpático e cuidadoso com o pedido.",
        "Massa artesanal com molho rico em sabor.",
        "Salada fresca com ingredientes de qualidade.",
        "Lanche com pão macio e ingredientes generosos.",
        "Comida chegou quente e bem embalada.",
        "Pedi pela segunda vez e manteve a qualidade.",
        "Restaurante caprichado nos detalhes. Vale o preço.",
        "Sushi bem preparado, arroz na textura ideal.",
        "Risoto cremoso na medida certa.",
        "Churrasco macio e bem temperado.",
        "Porção familiar com excelente custo-benefício.",
    ],
    5: [
        "Melhor restaurante que já pedi. Voltarei com certeza.",
        "Perfeito! Exatamente como esperado.",
        "Entregou antes do prazo, tudo fresquinho!",
        "Pedi pela segunda vez e não decepcionou.",
        "Temperatura ideal na entrega, comida deliciosa.",
        "Simplesmente incrível! Melhor delivery que já experimentei.",
        "Qualidade de restaurante presencial em casa. Impressionante.",
        "Entrega relâmpago e comida na temperatura perfeita.",
        "Superou todas as expectativas. Nota máxima com folga.",
        "Frango suculento, molho incrível, embalagem perfeita.",
        "Nunca comi uma pizza tão crocante entregue em casa.",
        "Porção absurdamente generosa pelo preço cobrado.",
        "Cada detalhe do prato estava perfeito. Arte na cozinha.",
        "Entregou em 20 minutos e ainda com brinde. Excelente!",
        "Comida quente, bem temperada e porção farta. Perfeito.",
        "Salada fresquíssima, parecia colhida na hora.",
        "Sushi premium com peixe de qualidade superior.",
        "Melhor hambúrguer que já comi por delivery.",
        "Restaurante tratou o pedido com muito cuidado e carinho.",
        "Entregador gentil, comida impecável. Experiência 5 estrelas.",
        "Marmita completa, bem temperada e ainda quente.",
        "Risoto perfeito, cremoso e com ingredientes nobres.",
        "Atendimento rápido, comida excepcional. Recomendo a todos.",
        "Carne no ponto, molhos deliciosos e sobremesa de brinde.",
        "Voltei ao mesmo restaurante 5 vezes. Qualidade constante.",
        "Prato visivelmente feito com carinho. Sabor inigualável.",
    ],
}

# Distribuição realista de notas
DISTRIBUICAO_NOTAS = [1]*8 + [2]*12 + [3]*25 + [4]*30 + [5]*25


def gerar_data_aleatoria():
    inicio = datetime(2024, 1, 1)
    fim = datetime(2024, 12, 31, 23, 59)
    delta = fim - inicio
    segundos = random.randint(0, int(delta.total_seconds()))
    dt = inicio + timedelta(seconds=segundos)
    # Arredonda para hora cheia
    return dt.replace(minute=0, second=0).strftime("%Y-%m-%d %H:%M:%S")


def gerar_avaliacoes(n: int = 1600) -> pd.DataFrame:
    df_pedidos = pd.read_csv("data/pedidos.csv")

    # Garante que cada pedido tenha no máximo uma avaliação
    pedidos_sample = df_pedidos.sample(n=n, random_state=42).reset_index(drop=True)

    rows = []
    for i, (_, pedido) in enumerate(pedidos_sample.iterrows(), start=1):
        nota = random.choice(DISTRIBUICAO_NOTAS)
        comentarios_disponiveis = REVIEWS[nota]
        comentario = random.choice(comentarios_disponiveis)

        rows.append({
            "id_avaliacao": i,
            "id_pedido": int(pedido["id_pedido"]),
            "id_restaurante": int(pedido["id_restaurante"]),
            "nota": nota,
            "comentario": comentario,
            "criado_em": gerar_data_aleatoria(),
        })

    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = gerar_avaliacoes(1600)

    print(f"Total reviews: {len(df)}")
    print(f"Textos únicos: {df['comentario'].nunique()}")
    print(f"\nDistribuição de notas:")
    print(df["nota"].value_counts().sort_index())
    print(f"\nTop 5 mais repetidos:")
    print(df["comentario"].value_counts().head(5))

    df.to_csv("data/avaliacoes.csv", index=False)
    print("\nCSV salvo em data/avaliacoes.csv")
