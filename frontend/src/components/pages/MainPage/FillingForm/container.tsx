import { connect } from "react-redux";
import Action from "../../../../types/Action";
import mainPageAC from "../../../../store/actionCreators/mainPageAC";
import MainDataFillingForm from "./MainDataFillingForm";

function mapDispatchToProps(dispatch: (action: Action) => void) {
    return{
        getData: (
            index_name: string,
            start_date: string,
            end_date: string,
            reduction: string,
            tolerance?: string,
            prefix?: string
        ) => {
            dispatch(
                mainPageAC.getAllData(
                    index_name,
                    start_date,
                    end_date,
                    reduction,
                    tolerance,
                    prefix
                )
            );
        },

        getExcelData: (
            index_name: string,
            start_date: string,
            end_date: string,
            reduction: string,
            tolerance?: string,
            prefix?: string
        ) => {
            dispatch(
                mainPageAC.getExcelData(
                    index_name,
                    start_date,
                    end_date,
                    reduction,
                    tolerance,
                    prefix
                )
            );
        }
    }
}

const Main_DataFillingFormContainer = connect(null, mapDispatchToProps)(MainDataFillingForm)

export default Main_DataFillingFormContainer