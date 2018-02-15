/***************************************************************************

 Copyright (c) 2018, EPAM SYSTEMS INC

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.

 ****************************************************************************/

package com.epam.dlab.automation.test.libs;

import com.epam.dlab.automation.helper.NamingHelper;

public class LibsHelper {
	private static final String LIB_GROUPS_JSON = "lib_groups.json";
	private static final String LIB_LIST_JSON = "lib_list.json";

    private static int currentQuantityOfLibInstallErrorsToFailTest;
    private static int maxQuantityOfLibInstallErrorsToFailTest;


    public static int getCurrentQuantityOfLibInstallErrorsToFailTest() {
        return currentQuantityOfLibInstallErrorsToFailTest;
    }

    public static void setCurrentQuantityOfLibInstallErrorsToFailTest(int currentQuantityOfLibInstallErrorsToFailTest) {
        LibsHelper.currentQuantityOfLibInstallErrorsToFailTest = currentQuantityOfLibInstallErrorsToFailTest;
    }

    public static int getMaxQuantityOfLibInstallErrorsToFailTest() {
        return maxQuantityOfLibInstallErrorsToFailTest;
    }

    public static void setMaxQuantityOfLibInstallErrorsToFailTest(int maxQuantityOfLibInstallErrorsToFailTest) {
        LibsHelper.maxQuantityOfLibInstallErrorsToFailTest = maxQuantityOfLibInstallErrorsToFailTest;
    }

    public static void incrementByOneCurrentQuantityOfLibInstallErrorsToFailTest(){
        currentQuantityOfLibInstallErrorsToFailTest++;
    }

    public static String getLibGroupsPath(String notebookName){
		if (notebookName.contains(NamingHelper.DEEPLEARNING)) {
			return NamingHelper.DEEPLEARNING + "/" + LIB_GROUPS_JSON;
		} else if (notebookName.contains(NamingHelper.JUPYTER)) {
			return NamingHelper.JUPYTER + "/" + LIB_GROUPS_JSON;
		} else if (notebookName.contains(NamingHelper.RSTUDIO)) {
			return NamingHelper.RSTUDIO + "/" + LIB_GROUPS_JSON;
		} else if (notebookName.contains(NamingHelper.TENSOR)) {
			return NamingHelper.TENSOR + "/" + LIB_GROUPS_JSON;
		} else if (notebookName.contains(NamingHelper.ZEPPELIN)) {
			return NamingHelper.ZEPPELIN + "/" + LIB_GROUPS_JSON;
		} else return LIB_GROUPS_JSON;
    }

    public static String getLibListPath(String notebookName){
		if (notebookName.contains(NamingHelper.DEEPLEARNING)) {
			return NamingHelper.DEEPLEARNING + "/" + LIB_LIST_JSON;
		} else if (notebookName.contains(NamingHelper.JUPYTER)) {
			return NamingHelper.JUPYTER + "/" + LIB_LIST_JSON;
		} else if (notebookName.contains(NamingHelper.RSTUDIO)) {
			return NamingHelper.RSTUDIO + "/" + LIB_LIST_JSON;
		} else if (notebookName.contains(NamingHelper.TENSOR)) {
			return NamingHelper.TENSOR + "/" + LIB_LIST_JSON;
		} else if (notebookName.contains(NamingHelper.ZEPPELIN)) {
			return NamingHelper.ZEPPELIN + "/" + LIB_LIST_JSON;
		} else return LIB_LIST_JSON;
    }
}
