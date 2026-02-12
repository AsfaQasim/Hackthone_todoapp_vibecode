import { NextResponse } from 'next/server';

// Hardcoded tasks for testing - directly from database
const HARDCODED_TASKS = [
  {
    id: "e7dc0cb3-b360-4eba-af4f-b0014b21ad12",
    title: "eating",
    description: "Created via AI Assistant",
    status: "pending",
    user_id: "add60fd1-792f-4ab9-9a53-e2f859482c59",
    created_at: "2026-02-07T00:00:00",
    updated_at: "2026-02-07T00:00:00"
  },
  {
    id: "74bfb68f-8643-4a89-992a-033dc292a387",
    title: "Eat",
    description: "Created via AI Assistant",
    status: "pending",
    user_id: "add60fd1-792f-4ab9-9a53-e2f859482c59",
    created_at: "2026-02-07T00:00:00",
    updated_at: "2026-02-07T00:00:00"
  },
  {
    id: "504823ae-e3af-46a3-826c-8b3d07ec718f",
    title: "eating in my general-task-execution",
    description: "Created via AI Assistant",
    status: "pending",
    user_id: "add60fd1-792f-4ab9-9a53-e2f859482c59",
    created_at: "2026-02-07T00:00:00",
    updated_at: "2026-02-07T00:00:00"
  }
];

export async function GET() {
  console.log('🧪 Returning hardcoded tasks for testing');
  return NextResponse.json(HARDCODED_TASKS);
}
