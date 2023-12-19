import { connect } from "react-redux";
import { CombinedState } from "redux";
import MainPageT from "../../../../types/MainPage";
import Charts from "./Charts";

function mapStateToProps(
    state: CombinedState<{
        main_page_table: MainPageT;
    }>
) {
    return {
        data: state.main_page_table.data,
    };
};

const ChartsContainer = connect(mapStateToProps, null)(Charts)

export default ChartsContainer