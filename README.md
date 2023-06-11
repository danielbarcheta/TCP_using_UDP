# redes-at3

Pequeno projeto para a Disciplina de Redes na USP que consiste
na simulação do protocolo de roteamento entre vários clientes e um servidor 
para o envio de múltiplas mensagens/pacotes

Para implementar uma funcionalidade semelhante ao TCP usando UDP, foram utilizados mecanismos de controle de fluxo, confiabilidade e retransmissão de pacotes ao código:

Controle de fluxo: Implementado um mecanismo para controlar a taxa de envio de pacotes para evitar sobrecarregar o receptor.

Confirmação de recebimento: O receptor deve enviar confirmações (acknowledgments) para o remetente indicando que um pacote foi recebido com sucesso.

Números de sequência: Adicionado números de sequência aos pacotes para garantir a ordem correta de entrega e permitir a detecção de pacotes perdidos ou duplicados.

Retransmissão de pacotes perdidos: Se o remetente não receber uma confirmação em um determinado período de tempo, ele deve retransmitir o pacote.

Controle de congestionamento: Implementado mecanismos para detectar e lidar com a congestão da rede, como reduzir a taxa de envio quando a rede está congestionada.
