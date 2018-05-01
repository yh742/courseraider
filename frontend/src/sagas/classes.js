import { put } from "redux-saga/effects";
// delete a user
export function* setSelectedClass(action) {
  // update the state by removing the user
  console.log(action, 'saga');
  action.callbackSuccess();
  // yield put({
  //   type: 'SET_SELECTED_CLASS',
  //   class_id: action.classes.class_Id,
  // });
}
