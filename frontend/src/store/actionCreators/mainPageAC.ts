import Action from "../../types/Action";
import ACTIONS from "./ACTIONS";


function getAllData(
    index_name: string,
    start_date: string,
    end_date: string,
    reduction: string,
    tolerance?: string,
    prefix?: string,
): Action {
    return {
        type: ACTIONS.GET_ALL_DATA,
        index_name: index_name,
        start_date: start_date,
        end_date: end_date,
        reduction: reduction,
        tolerance: tolerance ? tolerance : "0.05",
        prefix: prefix ? prefix : "CLOSE"
    };
}

function getExcelData(
    index_name: string,
    start_date: string,
    end_date: string,
    reduction: string,
    tolerance?: string,
    prefix?: string,
): Action {
    return {
        type: ACTIONS.GET_EXCEL_DATA,
        index_name: index_name,
        start_date: start_date,
        end_date: end_date,
        reduction: reduction,
        tolerance: tolerance ? tolerance : "0.05",
        prefix: prefix ? prefix : "CLOSE"
    };
}

function setAllData(
    data: any[],
): Action {
    return {
        type: ACTIONS.SET_ALL_DATA,
        data: data
    }
}


const mainPageAC = {
    getAllData: getAllData,
    setAllData: setAllData,
    getExcelData: getExcelData
};

export default mainPageAC;