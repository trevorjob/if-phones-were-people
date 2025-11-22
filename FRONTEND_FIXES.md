# Frontend Fixes - Usage Entry Component

## Date: November 16, 2025

## Issues Fixed

### 1. ✅ Wrong API Endpoint and Field Names

**Problem:**
- Frontend was calling `/usage/usage-data/bulk_upload/` which expects **UsageData** (device-level daily usage)
- But the form was trying to submit **AppUsage** (per-app usage tracking) data
- Field names didn't match the backend serializer

**Backend Models:**
- **UsageData**: Device-level daily metrics (total screen time, unlock count, etc.)
- **AppUsage**: Per-app usage tracking (time spent per app, launch count, etc.)

**Solution:**
1. Added new `appUsageAPI` to `services/api.ts`:
   ```typescript
   export const appUsageAPI = {
     list: (params?: any) => api.get('/usage/app-usage/', { params }),
     create: (data: any) => api.post('/usage/app-usage/', data),
     bulkCreate: (data: any[]) => api.post('/usage/app-usage/bulk_upload/', data),
   };
   ```

2. Updated `UsageEntry.tsx` to use correct API:
   - Changed import from `usageAPI` to `appUsageAPI`
   - Updated field names in state:
     - `usage_duration` → `time_spent_minutes`
     - `times_opened` → `launch_count`

3. Updated payload structure:
   ```typescript
   // Before (WRONG - UsageData format)
   {
     device: deviceId,           // ❌ Wrong endpoint
     device_app: entry.device_app,
     date: entry.date,
     usage_duration: entry.usage_duration,  // ❌ Wrong field name
     times_opened: entry.times_opened,      // ❌ Wrong field name
   }

   // After (CORRECT - AppUsage format)
   {
     device_app: entry.device_app,          // ✅ Correct field
     date: entry.date,
     time_spent_minutes: entry.time_spent_minutes,  // ✅ Correct field
     launch_count: entry.launch_count,               // ✅ Correct field
   }
   ```

### 2. ✅ Dropdown Visibility Issue

**Problem:**
- Select dropdown appeared transparent/invisible
- No proper styling for form inputs and select elements

**Solution:**
Added comprehensive form element styling to `UsageEntry.css`:

```css
.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  font-weight: 600;
  color: #333;
  font-size: 14px;
}

.form-group input,
.form-group select {
  padding: 10px 12px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 15px;
  font-family: inherit;
  background: white;
  color: #333;
  transition: border-color 0.2s;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-group select {
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23333' d='M6 9L1 4h10z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  padding-right: 36px;
}

.form-group select option {
  background: white;
  color: #333;
  padding: 8px;
}
```

**Features:**
- White background for visibility
- Custom dropdown arrow using SVG data URI
- Consistent styling with other form elements
- Focus states with purple highlight
- Proper option styling

## Files Modified

### 1. `client/src/services/api.ts`
- ✅ Added `appUsageAPI` with bulk_upload endpoint

### 2. `client/src/components/UsageEntry.tsx`
- ✅ Updated import to use `appUsageAPI`
- ✅ Changed field names: `usage_duration` → `time_spent_minutes`
- ✅ Changed field names: `times_opened` → `launch_count`
- ✅ Updated validation logic
- ✅ Fixed payload structure for AppUsage endpoint

### 3. `client/src/components/UsageEntry.css`
- ✅ Added `.form-group` styles
- ✅ Added label styling
- ✅ Added input and select styling
- ✅ Added custom dropdown arrow
- ✅ Added option element styling
- ✅ Added focus states
- ✅ Added disabled states

## Backend Endpoints Used

### AppUsage Bulk Upload
- **Endpoint:** `POST /api/usage/app-usage/bulk_upload/`
- **Serializer:** `AppUsageSerializer`
- **Required Fields:**
  - `device_app` (UUID) - ID of the DeviceApp
  - `date` (Date) - Date of usage
  - `time_spent_minutes` (Integer) - Minutes spent on app
  - `launch_count` (Integer) - Number of times opened

### Optional Fields
- `notification_count`
- `background_time_minutes`
- `session_count`
- `longest_session_minutes`
- `first_launch_time`
- `last_usage_time`
- `hourly_usage` (JSON array)

## Testing

### Before Testing
1. ✅ Django backend running on `http://localhost:8000`
2. ✅ Vite dev server running on `http://localhost:5173`
3. ✅ User registered and logged in
4. ✅ Device created with personality
5. ✅ Apps installed on device

### Test Flow
1. Navigate to dashboard
2. Click "Enter Usage" on a device
3. Verify dropdown is now visible with white background
4. Select an app from dropdown
5. Enter time spent (minutes)
6. Enter launch count
7. Click "Submit"
8. Verify success message
9. Check backend to confirm AppUsage records were created

### Success Criteria
- ✅ Dropdown is fully visible and styled
- ✅ Form submits without errors
- ✅ Backend receives correct payload format
- ✅ AppUsage records are created in database
- ✅ User redirected to dashboard after submission

## Notes

### Pre-existing TypeScript Warnings
The following TypeScript linting warnings exist but don't affect functionality:
- `Unexpected any` warnings in api.ts and UsageEntry.tsx
- React Hook dependency warnings

These are style/linting issues, not runtime errors.

### API Design Clarification
- **UsageData**: For device-level daily statistics (total screen time per day)
  - Endpoint: `/api/usage/usage-data/bulk_upload/`
  - Use this for overall device usage metrics
  
- **AppUsage**: For per-app usage tracking (time spent per app per day)
  - Endpoint: `/api/usage/app-usage/bulk_upload/`
  - Use this for app-specific usage data ← **What we're using**

## Next Steps (Optional)

1. **Add more AppUsage fields** - Extend form to collect:
   - Session count
   - Notification count
   - Background time
   - First/last launch time

2. **Add UsageData entry form** - Create separate form for device-level metrics:
   - Total screen time
   - Unlock count
   - Pickup count
   - Battery levels

3. **Batch date entry** - Allow entering multiple days of usage at once

4. **Usage history view** - Display previously entered usage data

5. **Validation improvements** - Add date range validation, duplicate detection

## Summary

Both issues have been successfully fixed:
1. ✅ **API Payload Issue**: Now using correct endpoint (`/app-usage/bulk_upload/`) with proper field names
2. ✅ **Dropdown Visibility**: Added comprehensive CSS styling for all form elements

The frontend can now successfully submit app usage data to the backend! 🎉
