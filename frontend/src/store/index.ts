import {applyMiddleware, CombinedState, combineReducers, createStore, Store } from "redux";

import MainPageT from "../types/MainPage";

import logger from "redux-logger";
import createSagaMiddleware from "redux-saga";

import Action from "../types/Action";

import watchGetAllData from "./sagas/getAllData";
import main_table from "./reducers/main_page_reducer";

const reducers = combineReducers({
    main_page_table: main_table
});

const saga = createSagaMiddleware();


let store: Store<
    CombinedState<{
        main_page_table: MainPageT;
    }>,
    Action> = createStore(reducers, applyMiddleware(logger, saga));

saga.run(watchGetAllData);

export default store;