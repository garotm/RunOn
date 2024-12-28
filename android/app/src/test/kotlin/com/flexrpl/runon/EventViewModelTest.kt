package com.flexrpl.runon

import com.flexrpl.runon.data.repository.EventRepository
import com.flexrpl.runon.domain.model.Event
import com.flexrpl.runon.ui.EventViewModel
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.flowOf
import kotlinx.coroutines.test.StandardTestDispatcher
import kotlinx.coroutines.test.TestScope
import kotlinx.coroutines.test.resetMain
import kotlinx.coroutines.test.runTest
import kotlinx.coroutines.test.setMain
import org.junit.After
import org.junit.Assert.assertEquals
import org.junit.Before
import org.junit.Test
import org.mockito.kotlin.mock
import org.mockito.kotlin.whenever

@OptIn(ExperimentalCoroutinesApi::class)
class EventViewModelTest {
    private val testDispatcher = StandardTestDispatcher()
    private val testScope = TestScope(testDispatcher)
    private val repository: EventRepository = mock()
    private lateinit var viewModel: EventViewModel
    private val testEvents = listOf(
        Event("1", "Test Event", "Description", "2024-02-14", "Location")
    )

    @Before
    fun setup() {
        whenever(repository.getEvents()).thenReturn(flowOf(testEvents))
        Dispatchers.setMain(testDispatcher)
        viewModel = EventViewModel(repository)
    }

    @After
    fun tearDown() {
        Dispatchers.resetMain()
    }

    @Test
    fun `events are loaded from repository`() = testScope.runTest {
        val actual = viewModel.events.first()
        assertEquals(testEvents, actual)
    }
}
