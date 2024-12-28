package com.flexrpl.runon.ui

import androidx.lifecycle.ViewModel
import com.flexrpl.runon.data.repository.EventRepository
import kotlinx.coroutines.flow.StateFlow

class EventViewModel(
    private val repository: EventRepository
) : ViewModel() {
    val events = repository.getEvents()
}
