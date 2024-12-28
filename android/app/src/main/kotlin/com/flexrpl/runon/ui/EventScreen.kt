package com.flexrpl.runon.ui

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Card
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.flexrpl.runon.domain.model.Event

@Composable
fun EventScreen(viewModel: EventViewModel) {
    Surface(color = MaterialTheme.colorScheme.background) {
        val events by viewModel.events.collectAsState(initial = emptyList())
        EventList(events = events)
    }
}

@Composable
private fun EventList(events: List<Event>) {
    LazyColumn {
        items(events) { event ->
            EventCard(event = event)
        }
    }
}

@Composable
private fun EventCard(event: Event) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(8.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = event.title,
                style = MaterialTheme.typography.titleMedium
            )
            Text(
                text = event.date,
                style = MaterialTheme.typography.bodyMedium
            )
            Text(
                text = event.location,
                style = MaterialTheme.typography.bodySmall
            )
        }
    }
}
