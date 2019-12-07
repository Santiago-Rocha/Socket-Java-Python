import os
import re
import sys
import tensorflow as tf
import socket


from settings import PROJECT_ROOT
from ACA.chatbot.botpredictor import BotPredictor

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
HOST = "localhost"
PORT = 9999

def bot_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((HOST, PORT))
    except socket.error as err:
        print('Bind failed. Error Code : ' .format(err))
        
    s.listen(10)
    print("Socket Listening")
    conn, addr = s.accept()

    """ 
        En las variables dir se ubican principalmente los datasets que se van a usar 
        para los entrenamientos y las reglas. 
        corp_dir -> Corpus de data para entrenar el chatbot.
        knbs_dir -> Corpus de entrenamiento con Jokes y Stories.
        res_dir -> Directorio resultado donde se guardan los resultados (Entrenamientos).
        rules_dir -> Directorio donde están ubicadas las reglas.
    """
    global predictor, session_id
    corp_dir = os.path.join(PROJECT_ROOT, 'ACA', 'Data', 'Corpus')
    knbs_dir = os.path.join(PROJECT_ROOT, 'ACA', 'Data', 'Variety')
    res_dir = os.path.join(PROJECT_ROOT, 'ACA', 'Data', 'Result')
    rules_dir = os.path.join(PROJECT_ROOT, 'ACA', 'Data', 'Rules')

    with tf.Session() as sess:
        predictor = BotPredictor(sess, corpus_dir=corp_dir, knbase_dir=knbs_dir,
                                 result_dir=res_dir, aiml_dir=rules_dir,
                                 result_file='basic')
        
        session_id = predictor.session_data.add_session()

        
        #sys.stdout.write(ans)
        
        while(True):
            question = conn.recv(1024).decode(encoding='UTF-8')
            ans = re.sub(r'_nl_|_np_', '\n', predictor.predict(session_id, question)).strip()
            sys.stdout.write(question)
            sys.stdout.flush()
            conn.send(bytes(ans+"\r\n",'UTF-8'))


if __name__ == "__main__":
    bot_socket()
