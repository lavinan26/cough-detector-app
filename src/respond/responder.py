
def respond(result,logging):
    if result == 'cough':
        logging.info("Cough detected")
    elif result == 'non_cough':
        logging.info("...")
    else:
        logging.info("Unexpected result")