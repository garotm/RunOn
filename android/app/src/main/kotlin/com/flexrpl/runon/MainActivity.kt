package com.flexrpl.runon

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.flexrpl.runon.data.repository.EventRepositoryImpl
import com.flexrpl.runon.ui.EventScreen
import com.flexrpl.runon.ui.EventViewModel

class MainActivity : ComponentActivity() {
    private val viewModel by lazy {
        val repository = EventRepositoryImpl()
        ViewModelProvider(this, EventViewModelFactory(repository))[EventViewModel::class.java]
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            EventScreen(viewModel)
        }
    }
}

class EventViewModelFactory(
    private val repository: EventRepositoryImpl
) : ViewModelProvider.Factory {
    @Suppress("UNCHECKED_CAST")
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(EventViewModel::class.java)) {
            return EventViewModel(repository) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}
