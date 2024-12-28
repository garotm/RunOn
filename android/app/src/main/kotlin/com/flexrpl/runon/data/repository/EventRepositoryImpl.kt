package com.flexrpl.runon.data.repository

import com.flexrpl.runon.domain.model.Event
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flowOf

class EventRepositoryImpl : EventRepository {
    override fun getEvents(): Flow<List<Event>> = flowOf(
        listOf(
            Event("1", "Morning Run", "5K run in the park", "2024-02-14", "Central Park"),
            Event("2", "Evening Jog", "Easy 3K", "2024-02-15", "Riverside")
        )
    )
}
