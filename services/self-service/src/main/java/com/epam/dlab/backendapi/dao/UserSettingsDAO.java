/***************************************************************************

 Copyright (c) 2016, EPAM SYSTEMS INC

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

package com.epam.dlab.backendapi.dao;

import com.epam.dlab.auth.UserInfo;
import com.epam.dlab.backendapi.resources.dto.UserAllowedBudgetDTO;
import io.dropwizard.auth.Auth;
import org.apache.commons.lang3.StringUtils;

import java.util.Optional;

import static com.epam.dlab.backendapi.dao.MongoCollections.USER_SETTINGS;
import static com.mongodb.client.model.Filters.eq;
import static com.mongodb.client.model.Updates.set;

/**
 * DAO for the user preferences.
 */
public class UserSettingsDAO extends BaseDAO {
	private static final String USER_UI_SETTINGS_FIELD = "userUISettings";
	private static final String USER_ALLOWED_BUDGET = "allowedBudget";

	/**
	 * Returns the user preferences of UI dashboard.
	 *
	 * @param userInfo user info.
	 * @return JSON content.
	 */
	public String getUISettings(@Auth UserInfo userInfo) {
		return findOne(USER_SETTINGS, eq(ID, userInfo.getName()))
				.map(d -> d.getString(USER_UI_SETTINGS_FIELD))
				.orElse(StringUtils.EMPTY);
	}

	/**
	 * Store the user preferences of UI dashboard.
	 *
	 * @param userInfo user info.
	 * @param settings user preferences in JSON format.
	 */
	public void setUISettings(UserInfo userInfo, String settings) {
		updateOne(USER_SETTINGS,
				eq(ID, userInfo.getName()),
				set(USER_UI_SETTINGS_FIELD, settings),
				true);
	}

	public void updateBudget(UserAllowedBudgetDTO allowedBudgetDTO) {
		updateOne(USER_SETTINGS,
				eq(ID, allowedBudgetDTO.getName()),
				set(USER_ALLOWED_BUDGET, allowedBudgetDTO.getBudget()),
				true);
	}

	public Optional<Long> getAllowedBudget(String user) {
		return findOne(USER_SETTINGS, eq(ID, user))
				.flatMap(d -> Optional.ofNullable(d.getLong(USER_ALLOWED_BUDGET)));
	}

}