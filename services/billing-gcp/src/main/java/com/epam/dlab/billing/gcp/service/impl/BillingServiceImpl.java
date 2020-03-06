/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

package com.epam.dlab.billing.gcp.service.impl;

import com.epam.dlab.billing.gcp.dao.BillingDAO;
import com.epam.dlab.billing.gcp.model.GcpBillingData;
import com.epam.dlab.billing.gcp.repository.BillingRepository;
import com.epam.dlab.billing.gcp.service.BillingService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
@Slf4j
public class BillingServiceImpl implements BillingService {
	private static final String USAGE_DATE_FORMAT = "yyyy-MM";

	private final BillingDAO billingDAO;
	private final BillingRepository billingRepository;

	@Autowired
	public BillingServiceImpl(BillingDAO billingDAO, BillingRepository billingRepository) {
		this.billingDAO = billingDAO;
		this.billingRepository = billingRepository;
	}

	@Override
	public void updateBillingData() {
		try {
			Map<String, List<GcpBillingData>> billingData = billingDAO.getBillingData()
					.stream()
					.collect(Collectors.groupingBy(bd -> bd.getUsageDate().substring(0, USAGE_DATE_FORMAT.length())));

			billingData.forEach((usageDate, billingDataList) -> {
				log.info("Updating billing information for month {}", usageDate);
				billingRepository.deleteByUsageDateRegex("^" + usageDate);
				billingRepository.insert(billingDataList);
			});
		} catch (Exception e) {
			log.error("Can not update billing due to: {}", e.getMessage(), e);
		}
	}
}
