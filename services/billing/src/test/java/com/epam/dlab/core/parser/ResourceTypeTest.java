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

package com.epam.dlab.core.parser;

import static junit.framework.TestCase.assertEquals;

import org.junit.Test;

public class ResourceTypeTest {
	
	@Test
	public void test() {
		ResourceType type = ResourceType.of("cluster");
		
		assertEquals(ResourceType.CLUSTER, type);
		assertEquals(ResourceType.CLUSTER.toString(), "CLUSTER");
	}
}
