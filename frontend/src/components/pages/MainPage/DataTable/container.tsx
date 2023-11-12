import { connect } from "react-redux";
import { CombinedState } from "redux";
import MainPageT from "../../../../types/MainPage";
import MainDataTable from "./MainDataTable";

function mapStateToProps(
    state: CombinedState<{
        main_page_table: MainPageT;
    }>
) {
    return {
        data: state.main_page_table.data,
        onLoad: state.main_page_table.OnLoad,
    };
};

const MainDataTableContainer = connect(mapStateToProps, null)(MainDataTable)

export default MainDataTableContainer