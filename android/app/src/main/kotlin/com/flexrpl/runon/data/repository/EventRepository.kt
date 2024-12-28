package com.flexrpl.runon.data.repository

import com.flexrpl.runon.domain.model.Event
import kotlinx.coroutines.flow.Flow

interface EventRepository {
    fun getEvents(): Flow<List<Event>>
}
