from selenium import webdriver
import threading
import time
import book_engines.bovada



def run():
    book_engine = {'bovada': book_engines.bovada_engine.bovada_engine(),
                   'maverick': book_engines.maverick_engine.maverick_engine()}


if __name__ == '__main__':
    run()