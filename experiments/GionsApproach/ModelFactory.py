from keras.models import Sequential
from keras.layers import Dense


class ModelFactory:
    @staticmethod
    def create():
        model = Sequential()
        model.add(Dense(units=768, activation='relu'))
        model.add(Dense(units=1000, activation='relu'))
        model.add(Dense(units=4100, activation='relu'))
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        return model

