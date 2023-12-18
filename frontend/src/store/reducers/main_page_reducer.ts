import Action from "../../types/Action";
import MainPageT from "../../types/MainPage";
import ACTIONS from "../actionCreators/ACTIONS";
import initialstate from "../states/main_page_table"


function convertTime(unixtime) {
    let date = new Date(unixtime)
    let month = date.getMonth() + 1
    return date.getDate() + "." + month +"." + date.getFullYear()
    };

function main_table(state: MainPageT = initialstate, action: Action): MainPageT {
    switch (action.type) {
        case ACTIONS.SET_ALL_DATA:
            for(let i=0; i<action.data.length; i++){
                action.data[i][0] = convertTime(action.data[i][0])
            }
            return {
                ...state,
                OnLoad: false,
                data: action.data
            };
    }
    return state;
}

export default main_table;